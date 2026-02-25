from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.config import settings

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -----------------------------
# SIGNUP
# -----------------------------
@router.post("/signup")
def signup(user_data: dict, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data["email"],
        full_name=user_data.get("full_name"),
        hashed_password=hash_password(user_data["password"]),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User signup successful: email={new_user.email}")

    return {"message": "User created successfully"}


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token({"sub": str(user.id)})
    logger.info(f"User login successful: email={user.email}")

    return {"access_token": access_token, "token_type": "bearer"}


# -----------------------------
# GET CURRENT USER
# -----------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    return user