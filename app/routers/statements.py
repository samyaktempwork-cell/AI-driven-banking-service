from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.services import statement_service
from app.routers.auth import get_current_user

router = APIRouter(prefix="/statements", tags=["Statements"])


@router.get("/account/{account_id}")
def get_statement(
    account_id: int,
    from_date: datetime = Query(...),
    to_date: datetime = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return statement_service.generate_statement(
        db,
        user.id,
        account_id,
        from_date,
        to_date
    )