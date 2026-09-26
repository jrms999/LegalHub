# LegalHub

**Status: early LawTech prototype.** This repository explores a guided claim intake flow for Scotland and England and Wales. It has a Next.js wizard and a FastAPI/SQLAlchemy backend for storing claim details and generating draft text files. The generated documents are currently **one-line placeholder templates** and are not suitable for filing with a court.

The goal is to make legal-form preparation easier to follow, including for people who benefit from plain language and a step-by-step process. The prototype does not give legal advice or decide whether a claim is appropriate.

## What is in the repository

- `legalhub/frontend`: Next.js 14 and TypeScript pages for Scotland and England and Wales claim intake.
- `legalhub/backend`: FastAPI claim CRUD, SQLAlchemy models, and draft text generation.
- `legalhub/backend/templates.py`: placeholder Jinja templates, not court forms.

## Current limitations

- The backend uses a hard-coded local PostgreSQL URL in `database.py`; no database or migration setup is supplied.
- `get_current_user_id()` returns user ID `1`. There is no real login or separation between users.
- The frontend expects an API at `http://localhost:8000` and does not yet expose configuration for another address.
- Generated outputs are short placeholders, with no validation against current court rules or independent legal review.
- No automated test suite or deployable production configuration is included.

Do not enter real personal case information into a shared or publicly reachable deployment of this prototype.

## Development path

1. Make local startup reproducible with environment-based database configuration and corrected Python package/dependency setup.
2. Define one narrow Scotland Simple Procedure intake journey with validated fields and safe example data.
3. Generate a useful **draft** summary and timeline, reviewed against official court guidance before any broader claim.
4. Add user authentication, access controls, tests, and a privacy review before accepting real case data.
5. Document an England and Wales flow separately, including its own rules and templates.

For the current code layout, see [`legalhub/README.md`](legalhub/README.md). Its earlier run command is being replaced here because the backend uses package-relative imports and requires a configured database. This repository is a development prototype, not a court filing service.
