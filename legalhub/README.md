# Code layout

The [root README](../README.md) has tested local setup instructions and current limitations.

- `backend/main.py`: FastAPI routes and a shared local demo identity (no authentication).
- `backend/database.py`, `models.py`, `schemas.py`, `crud.py`: SQLite by default, data models, validation and persistence.
- `backend/services/doc_generation.py`, `templates.py`: draft plain-text files. Scotland has a substantive summary, item list and timeline; England and Wales outputs remain placeholders.
- `backend/tests.py`: fictional-data API smoke test.
- `frontend`: Next.js 14 intake wizard; the API URL is fixed to localhost for this demo.
