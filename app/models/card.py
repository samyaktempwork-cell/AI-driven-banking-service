import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CardStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    card_number_hash = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.ACTIVE)

    daily_limit = Column(Float, default=5000.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="cards")