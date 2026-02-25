from pydantic import BaseModel
from datetime import date
from typing import Optional


class CardCreate(BaseModel):
    account_id: int
    expiry_date: date
    daily_limit: Optional[float] = 5000.0


class CardResponse(BaseModel):
    id: int
    account_id: int
    expiry_date: date
    status: str
    daily_limit: float

    class Config:
        orm_mode = True