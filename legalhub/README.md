# LawTech Claims Stack

Minimal starter stack for a LawTech app that helps prepare:

- Simple Procedure claims in Scotland
- Small / money claims in England & Wales (LBC + particulars)

## Backend

Python + FastAPI + SQLAlchemy + Postgres.

Run:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Update `DATABASE_URL` in `backend/database.py` to point at your Postgres instance.

## Frontend

Next.js + TypeScript.

Run:

```bash
cd frontend
npm install
npm run dev
```

The frontend assumes the API is running at `http://localhost:8000`.
