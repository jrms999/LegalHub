backend/

main.py (FastAPI app + routes)

database.py (SQLAlchemy engine/session)

models.py (Claim, Party, etc.)

schemas.py (Pydantic models)

crud.py (DB operations)

services/doc_generation.py (simple Jinja2-based text doc generator)

templates.py (placeholder Jinja2 templates)

requirements.txt

frontend/

Next.js 14 + TypeScript app

Wizards for:

/claims/new/scotland

/claims/new/england-wales

Simple ClaimWizard component and API helper
