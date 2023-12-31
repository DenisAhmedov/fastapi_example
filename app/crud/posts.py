from sqlalchemy.orm import Session

from app.models import Post, User
import app.schemas as schemas


def get_post(db: Session, post_id: int):
    return db.query(Post).get(post_id)


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate, author_id: int):
    db_post = Post(**post.dict(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post: Post, data: schemas.PostUpdate):
    post.title = data.title
    post.text = data.text
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()


def give_like(db: Session, post: Post, user: User):
    post.whom_likes.append(user)
    db.add(post)
    db.commit()


def give_dislike(db: Session, post: Post, user: User):
    post.whom_dislikes.append(user)
    db.add(post)
    db.commit()


def remove_like(db: Session, post: Post, user: User):
    post.whom_likes.remove(user)
    db.add(post)
    db.commit()


def remove_dislike(db: Session, post: Post, user: User):
    post.whom_dislikes.remove(user)
    db.add(post)
    db.commit()





