from typing import List

from sqlalchemy.orm import Session

from app.dao import get_post, get_posts
from app.depends import get_db, get_current_active_user
from app.schemas import Post
from fastapi import Depends
from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/", response_model=List[Post])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=Post)
def get_post(post_id, db: Session = Depends(get_db)):
    posts = get_post(db, post_id)
    return posts


