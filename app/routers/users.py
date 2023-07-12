from typing import List

from sqlalchemy.orm import Session

from app.crud import (get_posts_by_author, get_user, get_user_by_username,
                      get_users)
from app.database import get_db
from app.schemas import Post, User, UserCreate
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/posts", response_model=List[Post])
def read_items(user_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts_by_author(db, author_id=user_id, skip=skip, limit=limit)
    return posts
