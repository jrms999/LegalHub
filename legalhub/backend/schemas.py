from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .models import Jurisdiction, PartyRole


class PartyBase(BaseModel):
    role: PartyRole
    is_company: bool = False
    name: str
    address_line1: str
    address_line2: Optional[str] = None
    town_city: str
    postcode: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    other_names: Optional[str] = None


class PartyCreate(PartyBase):
    pass


class Party(PartyBase):
    id: int

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    event_date: Optional[date] = None
    title: str
    description: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class LossItemBase(BaseModel):
    label: str
    amount: float
    date_incurred: Optional[date] = None


class LossItemCreate(LossItemBase):
    pass


class LossItem(LossItemBase):
    id: int

    class Config:
        from_attributes = True


class EvidenceItemBase(BaseModel):
    label: str
    type: Optional[str] = None
    reference: Optional[str] = None


class EvidenceItemCreate(EvidenceItemBase):
    pass


class EvidenceItem(EvidenceItemBase):
    id: int

    class Config:
        from_attributes = True


class ClaimBase(BaseModel):
    jurisdiction: Jurisdiction
    claim_type: str
    amount_claimed: float
    interest_requested: bool = False
    interest_rate: Optional[float] = None
    interest_from: Optional[date] = None
    facts_summary: str
    desired_outcome: str
    pre_action_steps: Optional[str] = None
    dispute_summary_one_liner: Optional[str] = None
    court_name: Optional[str] = None


class ClaimCreate(ClaimBase):
    parties: List[PartyCreate]
    events: List[EventCreate] = []
    loss_items: List[LossItemCreate] = []
    evidence_items: List[EvidenceItemCreate] = []


class ClaimUpdate(BaseModel):
    claim_type: Optional[str] = None
    amount_claimed: Optional[float] = None
    interest_requested: Optional[bool] = None
    interest_rate: Optional[float] = None
    interest_from: Optional[date] = None
    facts_summary: Optional[str] = None
    desired_outcome: Optional[str] = None
    pre_action_steps: Optional[str] = None
    dispute_summary_one_liner: Optional[str] = None
    court_name: Optional[str] = None
    status: Optional[str] = None


class Claim(ClaimBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    parties: List[Party]
    events: List[Event]
    loss_items: List[LossItem]
    evidence_items: List[EvidenceItem]

    class Config:
        from_attributes = True


class Document(BaseModel):
    id: int
    doc_type: str
    storage_path: str

    class Config:
        from_attributes = True
