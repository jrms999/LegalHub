# LegalHub

**Status: local, single-user LawTech prototype.** LegalHub explores a guided claim-intake flow for Scotland and England and Wales. The Next.js wizard saves a claim through FastAPI and can generate plain-text drafts. It is not a filing service, legal advice, or a source of court-ready forms.

## What works

- Scotland and England and Wales intake screens; claim CRUD backed by SQLAlchemy.
- SQLite local demo database by default; an optional `DATABASE_URL` can point to another SQLAlchemy-supported database with the corresponding driver installed.
- A local demo identity created on first request. This is **not authentication**: all requests share its records. Run only on your own computer using invented information.
- Scotland draft case summary, item list and timeline with fictional-data API smoke test. The England and Wales letter and particulars remain placeholders.

## Run locally

From the repository root (Python 3.10+):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r legalhub/backend/requirements.txt
uvicorn legalhub.backend.main:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
cd legalhub/frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend calls `http://localhost:8000`. The local database is `legalhub/backend/legalhub_demo.db`; generated draft text files are under `legalhub/backend/generated_docs/`. Both paths are git-ignored. To start fresh, stop the API and remove the demo database and generated drafts. `DATABASE_URL` can override the SQLite location; schema migrations are not implemented.

Run the backend smoke test from the repository root:

```bash
python -m unittest legalhub.backend.tests -v
```

The Scotland wizard currently reports generated document types, while draft files are saved locally by the API. It does not display or download the draft in the browser. Its England and Wales flow is less complete. Do not enter actual case details or expose this server publicly.

## Next engineering milestones

1. Add authenticated accounts, record-level authorisation, a privacy review and migration tooling before any multi-user use.
2. Show and download reviewed drafts in the UI, with editable facts and clear validation errors.
3. Check jurisdiction-specific requirements against authoritative guidance and obtain legal review before suggesting filing use.
4. Add end-to-end tests and deployment safeguards; do not treat this local demo as production-ready.
