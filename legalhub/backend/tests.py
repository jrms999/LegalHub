"""API smoke tests with an isolated, disposable SQLite database."""
import tempfile
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from legalhub.backend.database import Base, get_db
from legalhub.backend.main import app
from legalhub.backend import models  # noqa: F401 - registers tables


class ClaimFlowTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine)

        def test_db():
            with session_factory() as db:
                yield db

        app.dependency_overrides[get_db] = test_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def test_scotland_claim_and_draft(self):
        party = {"address_line1": "1 Example Street", "town_city": "Glasgow", "postcode": "G1 1AA"}
        payload = {
            "jurisdiction": "SCOTLAND", "claim_type": "DEBT", "amount_claimed": 120,
            "facts_summary": "A fictional invoice was not paid.",
            "desired_outcome": "Payment of the fictional balance.",
            "parties": [{**party, "role": "CLAIMANT", "name": "Alex Example", "email": ""},
                        {**party, "role": "DEFENDANT", "name": "Casey Example"}],
            "events": [{"event_date": "2026-01-01", "title": "Invoice", "description": "Fictional invoice sent."}],
            "loss_items": [{"label": "Invoice", "amount": 120}],
        }
        bad = {**payload, "amount_claimed": -1}
        self.assertEqual(self.client.post("/claims", json=bad).status_code, 422)
        result = self.client.post("/claims", json=payload)
        self.assertEqual(result.status_code, 200, result.text)
        claim_id = result.json()["id"]
        self.assertEqual(len(self.client.get("/claims").json()), 1)
        self.assertEqual(self.client.get(f"/claims/{claim_id}").json()["facts_summary"], payload["facts_summary"])
        # Generation writes disposable fictional output, never personal data.
        with tempfile.TemporaryDirectory() as folder:
            from legalhub.backend.services import doc_generation
            old_dir = doc_generation.DOCS_DIR
            doc_generation.DOCS_DIR = __import__("pathlib").Path(folder)
            try:
                response = self.client.post(f"/claims/{claim_id}/generate")
                self.assertEqual(response.status_code, 200, response.text)
                summary = (doc_generation.DOCS_DIR / f"claim_{claim_id}_scotland_summary.txt").read_text()
                self.assertIn("Alex Example", summary)
                self.assertIn("A fictional invoice was not paid.", summary)
                self.assertIn("FOR REVIEW ONLY", summary)
                self.assertEqual(len(self.client.get(f"/claims/{claim_id}/documents").json()), 3)
            finally:
                doc_generation.DOCS_DIR = old_dir


if __name__ == "__main__":
    unittest.main()
