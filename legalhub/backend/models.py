from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date,
    Float, ForeignKey, Enum, Text
)
from sqlalchemy.orm import relationship
import enum

from .database import Base


class Jurisdiction(str, enum.Enum):
    SCOTLAND = "SCOTLAND"
    ENGLAND_WALES = "ENGLAND_WALES"


class PartyRole(str, enum.Enum):
    CLAIMANT = "CLAIMANT"
    DEFENDANT = "DEFENDANT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    claims = relationship("Claim", back_populates="user")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    jurisdiction = Column(Enum(Jurisdiction), nullable=False)
    claim_type = Column(String, nullable=False)
    amount_claimed = Column(Float, nullable=False)
    interest_requested = Column(Boolean, default=False)
    interest_rate = Column(Float, nullable=True)
    interest_from = Column(Date, nullable=True)
    facts_summary = Column(Text, nullable=False)
    desired_outcome = Column(Text, nullable=False)
    pre_action_steps = Column(Text, nullable=True)
    dispute_summary_one_liner = Column(String, nullable=True)
    status = Column(String, default="DRAFT")
    court_name = Column(String, nullable=True)
    court_reference = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="claims")
    parties = relationship("Party", back_populates="claim", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="claim", cascade="all, delete-orphan")
    loss_items = relationship(
        "LossItem", back_populates="claim", cascade="all, delete-orphan"
    )
    evidence_items = relationship(
        "EvidenceItem", back_populates="claim", cascade="all, delete-orphan"
    )
    documents = relationship(
        "Document", back_populates="claim", cascade="all, delete-orphan"
    )


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    role = Column(Enum(PartyRole), nullable=False)
    is_company = Column(Boolean, default=False)
    name = Column(String, nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    town_city = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    other_names = Column(String, nullable=True)

    claim = relationship("Claim", back_populates="parties")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    event_date = Column(Date, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    claim = relationship("Claim", back_populates="events")


class LossItem(Base):
    __tablename__ = "loss_items"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    label = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date_incurred = Column(Date, nullable=True)

    claim = relationship("Claim", back_populates="loss_items")


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    label = Column(String, nullable=False)
    type = Column(String, nullable=True)
    reference = Column(String, nullable=True)

    claim = relationship("Claim", back_populates="evidence_items")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    doc_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    claim = relationship("Claim", back_populates="documents")
