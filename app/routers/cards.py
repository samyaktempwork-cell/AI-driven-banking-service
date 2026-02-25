from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.card import CardCreate, CardResponse
from app.services import card_service
from app.routers.auth import get_current_user
import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cards", tags=["Cards"])


@router.post("/", response_model=CardResponse)
def issue_card(
    data: CardCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    logger.info(f"Card issued: user={user.id}, account={data.account_id}")
    return card_service.create_card(db, user.id, data)


@router.patch("/{card_id}/block")
def block_card(
    card_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    logger.info(f"Card blocked: user={user.id}, card_id={card_id}")
    return card_service.block_card(db, user.id, card_id)


@router.get("/account/{account_id}", response_model=list[CardResponse])
def list_cards(
    account_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return card_service.list_cards(db, user.id, account_id)