import bcrypt
import random
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.card import Card, CardStatus
from app.models.account import Account


def generate_card_number() -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(16)])


def create_card(db: Session, user_id: int, data):
    account = db.query(Account).filter(Account.id == data.account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")


    if account.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    raw_card_number = generate_card_number()
    hashed = bcrypt.hashpw(raw_card_number.encode(), bcrypt.gensalt())

    card = Card(
        account_id=data.account_id,
        card_number_hash=hashed.decode(),
        expiry_date=data.expiry_date,
        daily_limit=data.daily_limit
    )

    db.add(card)
    db.commit()
    db.refresh(card)

    return card


def block_card(db: Session, user_id: int, card_id: int):
    card = db.query(Card).filter(Card.id == card_id).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")


    if card.account.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    card.status = CardStatus.BLOCKED
    db.commit()

    return {"message": "Card blocked successfully"}


def list_cards(db: Session, user_id: int, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")


    if account.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return db.query(Card).filter(Card.account_id == account_id).all()