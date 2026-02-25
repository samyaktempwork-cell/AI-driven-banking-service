from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.transaction import Transaction
from app.models.account import Account
from datetime import datetime


def generate_statement(
    db: Session,
    user_id: int,
    account_id: int,
    from_date: datetime,
    to_date: datetime,
):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Fetch all account transactions first
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).all()

    # Safe date filtering in Python
    filtered_transactions = [
        t for t in transactions
        if from_date <= t.created_at <= to_date
    ]

    total_debit = sum(
        t.amount for t in filtered_transactions
        if t.type.upper() == "DEBIT"
    )

    total_credit = sum(
        t.amount for t in filtered_transactions
        if t.type.upper() == "CREDIT"
    )

    return {
        "account_id": account_id,
        "from": from_date,
        "to": to_date,
        "transactions": filtered_transactions,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "closing_balance": account.balance
    }