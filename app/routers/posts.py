from typing import List

from sqlalchemy.orm import Session

from app.crud import get_post, get_posts
from app.database import get_db
from app.schemas import Post
from fastapi import Depends
from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=List[Post])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=Post)
def read_items(post_id, db: Session = Depends(get_db)):
    posts = get_post(db, post_id)
    return posts


