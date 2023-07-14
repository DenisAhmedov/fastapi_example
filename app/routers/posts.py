from typing import List

from sqlalchemy.orm import Session

from app import dao
from app.depends import get_db, get_current_active_user
from app.models import User
from app.schemas import Post, PostCreate, PostUpdate
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/", dependencies=[Depends(get_current_active_user)], response_model=List[Post])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = dao.get_posts(db, skip=skip, limit=limit)
    return posts


@router.post("/", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_active_user)):
    return dao.create_post(db=db, post=post, author_id=user.id)


@router.get("/{post_id}", dependencies=[Depends(get_current_active_user)], response_model=Post)
def get_post(post_id, db: Session = Depends(get_db)):
    post = dao.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=Post)
def update_post(post_id,
                data: PostUpdate,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_active_user)):
    post: Post = dao.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    elif post.author_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the author of the post")
    return dao.update_post(db=db, data=data, post=post)


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_active_user)):
    post: Post = dao.get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    elif post.author_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the author of the post")
    dao.delete_post(db=db, post=post)



