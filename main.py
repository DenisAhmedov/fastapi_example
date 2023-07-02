from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
import uvicorn

import crud, models, schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='example app on FastAPI')


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/users/", response_model=List[schemas.User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/posts/", response_model=List[schemas.Post])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/post/{post_id}/", response_model=schemas.Post)
def read_items(post_id, db: Session = Depends(get_db)):
    posts = crud.get_post(db, post_id)
    return posts


@app.get("/user/{user_id}/posts/", response_model=List[schemas.Post])
def read_items(user_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_author(db, author_id=user_id, skip=skip, limit=limit)
    return posts


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
