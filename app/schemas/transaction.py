from pydantic import BaseModel
from datetime import datetime


class DepositWithdrawRequest(BaseModel):
    account_id: int
    amount: float


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float


class TransactionResponse(BaseModel):
    id: int
    account_id: int
    related_account_id: int | None
    type: str
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True