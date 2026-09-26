# LegalHub code layout

This folder contains an early FastAPI backend and Next.js frontend. The [root README](../README.md) describes the prototype's current limits and intended development path.

## Backend (`backend/`)

- `main.py`: claim API routes. The current `get_current_user_id()` returns a fixed ID.
- `database.py`, `models.py`, `schemas.py`, `crud.py`: data access and claim models. The PostgreSQL URL is a local placeholder and must be configured before use.
- `services/doc_generation.py`, `templates.py`: text-file generation using one-line placeholder templates.

The earlier instruction to run `uvicorn main:app` from inside `backend/` does not match the package-relative imports in `main.py`. Local startup and database dependency wiring need verification before documenting a working run command.

## Frontend (`frontend/`)

- Next.js 14 with Scotland and England and Wales claim intake pages.
- `app/lib/api.ts` currently points to `http://localhost:8000`.

This is prototype code. Use fictional test data until authentication, privacy controls, document validation, and repeatable setup are in place.
