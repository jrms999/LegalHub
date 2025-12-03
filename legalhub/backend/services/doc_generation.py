from datetime import date
from pathlib import Path
from jinja2 import Template
from sqlalchemy.orm import Session

from .. import models, crud
from ..templates import (
    SCOTLAND_CLAIM_SUMMARY_TEMPLATE,
    SCHEDULE_OF_LOSS_TEMPLATE,
    TIMELINE_TEMPLATE,
    LBC_TEMPLATE,
    PARTICULARS_TEMPLATE,
)


DOCS_DIR = Path("generated_docs")
DOCS_DIR.mkdir(exist_ok=True)


def _render(template_str: str, context: dict) -> str:
    return Template(template_str).render(**context)


def _amount_totals(loss_items):
    principal = sum(li.amount for li in loss_items)
    return {
        "principal": principal,
        "interest_to_date": 0.0,
        "court_fee": 0.0,
        "other_costs": 0.0,
        "overall": principal,
    }


def build_context_for_claim(claim: models.Claim) -> dict:
    claimant = next(p for p in claim.parties if p.role.name == "CLAIMANT")
    defendant = next(p for p in claim.parties if p.role.name == "DEFENDANT")

    def full_address(p: models.Party) -> str:
        parts = [p.address_line1]
        if p.address_line2:
            parts.append(p.address_line2)
        parts.append(p.town_city)
        parts.append(p.postcode)
        return ", ".join(parts)

    loss_items = claim.loss_items
    totals = _amount_totals(loss_items)

    return {
        "today": date.today().isoformat(),
        "claimant": {
            "name": claimant.name,
            "address_full": full_address(claimant),
        },
        "defendant": {
            "name": defendant.name,
            "address_full": full_address(defendant),
        },
        "court": {
            "name": claim.court_name or "",
            "reference_or_blank": claim.court_reference or "",
        },
        "claim": {
            "amount_claimed": claim.amount_claimed,
            "dispute_summary_one_liner": claim.dispute_summary_one_liner or "",
            "facts_narrative": claim.facts_summary,
            "pre_action_steps": claim.pre_action_steps or "",
            "desired_outcome_text": claim.desired_outcome,
        },
        "loss_items": [
            {
                "label": li.label,
                "amount": li.amount,
                "date_or_unknown": li.date_incurred.isoformat()
                if li.date_incurred
                else "Unknown",
            }
            for li in loss_items
        ],
        "events": [
            {
                "date": ev.event_date.isoformat() if ev.event_date else "Unknown",
                "title": ev.title,
                "description": ev.description,
            }
            for ev in claim.events
        ],
        "evidence_items": [
            {
                "label": ei.label,
                "type": ei.type or "",
                "reference": ei.reference or "",
            }
            for ei in claim.evidence_items
        ],
        "respondents": [],
        "orders": [claim.desired_outcome],
        "totals": totals,
        "lbc_deadline_days": 14,
        "primary_respondent": {"name": defendant.name},
    }


def generate_documents_for_claim(db: Session, claim: models.Claim):
    context = build_context_for_claim(claim)
    docs = []

    if claim.jurisdiction.name == "SCOTLAND":
        summary_text = _render(SCOTLAND_CLAIM_SUMMARY_TEMPLATE, context)
        schedule_text = _render(SCHEDULE_OF_LOSS_TEMPLATE, context)
        timeline_text = _render(TIMELINE_TEMPLATE, context)

        summary_path = DOCS_DIR / f"claim_{claim.id}_scotland_summary.txt"
        schedule_path = DOCS_DIR / f"claim_{claim.id}_schedule.txt"
        timeline_path = DOCS_DIR / f"claim_{claim.id}_timeline.txt"

        summary_path.write_text(summary_text, encoding="utf-8")
        schedule_path.write_text(schedule_text, encoding="utf-8")
        timeline_path.write_text(timeline_text, encoding="utf-8")

        docs.append(crud.create_document(db, claim.id, "SCOTLAND_SUMMARY", str(summary_path)))
        docs.append(crud.create_document(db, claim.id, "SCHEDULE_OF_LOSS", str(schedule_path)))
        docs.append(crud.create_document(db, claim.id, "TIMELINE", str(timeline_path)))

    if claim.jurisdiction.name == "ENGLAND_WALES":
        lbc_text = _render(LBC_TEMPLATE, context)
        particulars_text = _render(PARTICULARS_TEMPLATE, context)
        schedule_text = _render(SCHEDULE_OF_LOSS_TEMPLATE, context)

        lbc_path = DOCS_DIR / f"claim_{claim.id}_lbc.txt"
        particulars_path = DOCS_DIR / f"claim_{claim.id}_particulars.txt"
        schedule_path = DOCS_DIR / f"claim_{claim.id}_schedule.txt"

        lbc_path.write_text(lbc_text, encoding="utf-8")
        particulars_path.write_text(particulars_text, encoding="utf-8")
        schedule_path.write_text(schedule_text, encoding="utf-8")

        docs.append(crud.create_document(db, claim.id, "LBC", str(lbc_path)))
        docs.append(crud.create_document(db, claim.id, "PARTICULARS", str(particulars_path)))
        docs.append(crud.create_document(db, claim.id, "SCHEDULE_OF_LOSS", str(schedule_path)))

    return docs
