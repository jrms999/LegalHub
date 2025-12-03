from sqlalchemy.orm import Session
from typing import List
from . import models, schemas


def create_claim(db: Session, user_id: int, claim_in: schemas.ClaimCreate) -> models.Claim:
    claim = models.Claim(
        user_id=user_id,
        jurisdiction=claim_in.jurisdiction,
        claim_type=claim_in.claim_type,
        amount_claimed=claim_in.amount_claimed,
        interest_requested=claim_in.interest_requested,
        interest_rate=claim_in.interest_rate,
        interest_from=claim_in.interest_from,
        facts_summary=claim_in.facts_summary,
        desired_outcome=claim_in.desired_outcome,
        pre_action_steps=claim_in.pre_action_steps,
        dispute_summary_one_liner=claim_in.dispute_summary_one_liner,
        status="DRAFT",
        court_name=claim_in.court_name,
    )
    db.add(claim)
    db.flush()

    for p in claim_in.parties:
        party = models.Party(
            claim_id=claim.id,
            **p.model_dump()
        )
        db.add(party)

    for ev in claim_in.events:
        db.add(models.Event(claim_id=claim.id, **ev.model_dump()))

    for li in claim_in.loss_items:
        db.add(models.LossItem(claim_id=claim.id, **li.model_dump()))

    for ei in claim_in.evidence_items:
        db.add(models.EvidenceItem(claim_id=claim.id, **ei.model_dump()))

    db.commit()
    db.refresh(claim)
    return claim


def get_claim(db: Session, claim_id: int, user_id: int) -> models.Claim | None:
    return (
        db.query(models.Claim)
        .filter(models.Claim.id == claim_id, models.Claim.user_id == user_id)
        .first()
    )


def list_claims(db: Session, user_id: int) -> List[models.Claim]:
    return (
        db.query(models.Claim)
        .filter(models.Claim.user_id == user_id)
        .order_by(models.Claim.created_at.desc())
        .all()
    )


def update_claim(db: Session, claim: models.Claim, updates: schemas.ClaimUpdate) -> models.Claim:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(claim, field, value)
    db.commit()
    db.refresh(claim)
    return claim


def create_document(db: Session, claim_id: int, doc_type: str, storage_path: str) -> models.Document:
    doc = models.Document(
        claim_id=claim_id,
        doc_type=doc_type,
        storage_path=storage_path
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def list_documents(db: Session, claim_id: int, user_id: int) -> List[models.Document]:
    return (
        db.query(models.Document)
        .join(models.Claim)
        .filter(models.Claim.user_id == user_id, models.Document.claim_id == claim_id)
        .all()
    )
