from pydantic import BaseModel
from datetime import datetime


class AccountCreate(BaseModel):
    currency: str = "USD"


class AccountResponse(BaseModel):
    id: int
    account_number: str
    balance: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True