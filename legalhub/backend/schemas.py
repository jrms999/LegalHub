from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from .models import Jurisdiction, PartyRole


class PartyBase(BaseModel):
    role: PartyRole
    is_company: bool = False
    name: str = Field(min_length=1, max_length=200)
    address_line1: str = Field(min_length=1, max_length=200)
    address_line2: Optional[str] = None
    town_city: str = Field(min_length=1, max_length=100)
    postcode: str = Field(min_length=1, max_length=20)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    other_names: Optional[str] = None

    @field_validator("email", mode="before")
    @classmethod
    def blank_email_is_missing(cls, value):
        return None if value == "" else value


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
    amount: float = Field(ge=0)
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
    amount_claimed: float = Field(ge=0)
    interest_requested: bool = False
    interest_rate: Optional[float] = None
    interest_from: Optional[date] = None
    facts_summary: str = Field(min_length=1)
    desired_outcome: str = Field(min_length=1)
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
