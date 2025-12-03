from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, get_db
from . import models, schemas, crud
from .services.doc_generation import generate_documents_for_claim

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LawTech Claims API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_current_user_id() -> int:
    return 1


@app.post("/claims", response_model=schemas.Claim)
def create_claim(
    claim_in: schemas.ClaimCreate,
    db: Session = Depends(get_db()),
    user_id: int = Depends(get_current_user_id),
):
    claim = crud.create_claim(db, user_id, claim_in)
    return claim


@app.get("/claims", response_model=List[schemas.Claim])
def list_user_claims(
    db: Session = Depends(get_db()),
    user_id: int = Depends(get_current_user_id),
):
    claims = crud.list_claims(db, user_id)
    return claims


@app.get("/claims/{claim_id}", response_model=schemas.Claim)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db()),
    user_id: int = Depends(get_current_user_id),
):
    claim = crud.get_claim(db, claim_id, user_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@app.patch("/claims/{claim_id}", response_model=schemas.Claim)
def update_claim(
    claim_id: int,
    updates: schemas.ClaimUpdate,
    db: Session = Depends(get_db()),
    user_id: int = Depends(get_current_user_id),
):
    claim = crud.get_claim(db, claim_id, user_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    claim = crud.update_claim(db, claim, updates)
    return claim


@app.post("/claims/{claim_id}/generate")
def generate_claim_documents(
    claim_id: int,
    db: Session = Depends(get_db()),
    user_id: int = Depends(get_current_user_id),
):
    claim = crud.get_claim(db, claim_id, user_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    docs = generate_documents_for_claim(db, claim)
    return {"generated": [d.doc_type for d in docs]}


@app.get("/claims/{claim_id}/documents", response_model=List[schemas.Document])
def list_claim_documents(
    claim_id: int,
    db: Session = Depends(get_db()),
    user_id: int = Depends(get_current_user_id),
):
    claim = crud.get_claim(db, claim_id, user_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return crud.list_documents(db, claim_id, user_id)
