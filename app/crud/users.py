import hashlib

from sqlalchemy.orm import Session

from app.models import User, Post
from app import schemas
from app.utils.auth import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        location=user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users_posts(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.author_id == author_id).offset(skip).limit(limit).all()
