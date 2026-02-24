from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", response_model=AccountResponse)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Generate unique account number
    account_number = str(uuid.uuid4()).replace("-", "")[:12]

    new_account = Account(
        account_number=account_number,
        user_id=current_user.id,
        balance=0.0,
        currency=account_data.currency,
        status="ACTIVE",
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


@router.get("", response_model=list[AccountResponse])
def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    accounts = (
        db.query(Account)
        .filter(Account.user_id == current_user.id)
        .all()
    )

    return accounts