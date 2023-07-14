from typing import List

from sqlalchemy.orm import Session

from app.dao import get_users_posts, get_user, create_user, get_user_by_username, get_users
from app.depends import get_db, get_current_active_user
from app.schemas import Post, User, UserCreate
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[User], dependencies=[Depends(get_current_active_user)])
def get_all_users_views(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user_views(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User, dependencies=[Depends(get_current_active_user)])
def get_user_views(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/posts", response_model=List[Post], dependencies=[Depends(get_current_active_user)])
def get_users_posts_views(user_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_users_posts(db, author_id=user_id, skip=skip, limit=limit)
    return posts
