import logging
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

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/deposit", response_model=TransactionResponse)
def deposit(data: DepositWithdrawRequest,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):

    account = db.query(Account).filter(
        Account.id == data.account_id,
        Account.user_id == current_user.id,
    ).first()

    if not account:
        logger.warning(f"Deposit failed: account not found user={current_user.id}")
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        logger.warning(f"Deposit failed: invalid amount user={current_user.id}")
        raise HTTPException(status_code=400, detail="Amount must be positive")

    account.balance += data.amount

    transaction = Transaction(
        account_id=account.id,
        related_account_id=None,
        type="CREDIT",
        amount=data.amount,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    logger.info(f"Deposit successful: user={current_user.id}, account={account.id}, amount={data.amount}")
    return transaction


@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(data: DepositWithdrawRequest,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):

    account = db.query(Account).filter(
        Account.id == data.account_id,
        Account.user_id == current_user.id,
    ).first()

    if not account:
        logger.warning(f"Withdraw failed: account not found user={current_user.id}")
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        logger.warning(f"Withdraw failed: invalid amount user={current_user.id}")
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if account.balance < data.amount:
        logger.warning(f"Withdraw failed: insufficient funds user={current_user.id}")
        raise HTTPException(status_code=400, detail="Insufficient balance")

    account.balance -= data.amount

    transaction = Transaction(
        account_id=account.id,
        related_account_id=None,
        type="DEBIT",
        amount=data.amount,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    logger.info(f"Withdraw successful: user={current_user.id}, account={account.id}, amount={data.amount}")
    return transaction


@router.post("/transfer", response_model=TransactionResponse)
def transfer(data: TransferRequest,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):

    if data.from_account_id == data.to_account_id:
        logger.warning("Transfer failed: same account")
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    from_account = db.query(Account).filter(
        Account.id == data.from_account_id,
        Account.user_id == current_user.id,
    ).first()

    if not from_account:
        logger.warning(f"Transfer failed: source not found user={current_user.id}")
        raise HTTPException(status_code=404, detail="Source account not found")

    to_account = db.query(Account).filter(
        Account.id == data.to_account_id,
    ).first()

    if not to_account:
        logger.warning("Transfer failed: destination not found")
        raise HTTPException(status_code=404, detail="Destination account not found")

    if from_account.balance < data.amount:
        logger.warning(f"Transfer failed: insufficient funds user={current_user.id}")
        raise HTTPException(status_code=400, detail="Insufficient balance")

    from_account.balance -= data.amount
    to_account.balance += data.amount

    transaction = Transaction(
        account_id=from_account.id,
        related_account_id=to_account.id,
        type="DEBIT",
        amount=data.amount,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    logger.info(f"Transfer successful: from={from_account.id}, to={to_account.id}, amount={data.amount}")
    return transaction