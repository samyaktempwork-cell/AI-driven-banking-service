from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import (
    DepositWithdrawRequest,
    TransferRequest,
    TransactionResponse,
)
from app.core.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/deposit", response_model=TransactionResponse)
def deposit(
    data: DepositWithdrawRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(
        Account.id == data.account_id,
        Account.user_id == current_user.id,
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    account.balance += data.amount

    transaction = Transaction(
        account_id=account.id,
        related_account_id=None,
        type="DEPOSIT",
        amount=data.amount,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(
    data: DepositWithdrawRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(
        Account.id == data.account_id,
        Account.user_id == current_user.id,
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if account.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    account.balance -= data.amount

    transaction = Transaction(
        account_id=account.id,
        related_account_id=None,
        type="WITHDRAW",
        amount=data.amount,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.post("/transfer", response_model=TransactionResponse)
def transfer(
    data: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.from_account_id == data.to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    from_account = db.query(Account).filter(
        Account.id == data.from_account_id,
        Account.user_id == current_user.id,
    ).first()

    if not from_account:
        raise HTTPException(status_code=404, detail="Source account not found")

    to_account = db.query(Account).filter(
        Account.id == data.to_account_id,
    ).first()

    if not to_account:
        raise HTTPException(status_code=404, detail="Destination account not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if from_account.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    from_account.balance -= data.amount
    to_account.balance += data.amount

    transaction = Transaction(
        account_id=from_account.id,
        related_account_id=to_account.id,
        type="TRANSFER",
        amount=data.amount,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

@router.get("/{account_id}", response_model=list[TransactionResponse])
def get_account_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id,
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    transactions = (
        db.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

    return transactions