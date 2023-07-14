from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.depends import get_db
from app.schemas import Token, UserCreate
from app.utils.auth import authenticate_user, create_access_token

router = APIRouter(
    prefix="/token",
    tags=["token"],
)


@router.post("/", response_model=Token)
async def login_for_access_token(user_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
