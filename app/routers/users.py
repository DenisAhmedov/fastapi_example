from typing import List

from sqlalchemy.orm import Session

from app import crud
from app.depends import get_db, get_current_active_user
from app.schemas import Post, User, UserCreate
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/', response_model=List[User], dependencies=[Depends(get_current_active_user)])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='username already registered')
    return crud.create_user(db=db, user=user)


@router.get('/my_posts', response_model=List[Post])
def get_my_posts(skip: int = 0,
                 limit: int = 100,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_active_user)):
    return crud.get_users_posts(db, author_id=user.id, skip=skip, limit=limit)


@router.get('/{user_id}', response_model=User, dependencies=[Depends(get_current_active_user)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.get('/{user_id}/posts', response_model=List[Post], dependencies=[Depends(get_current_active_user)])
def get_users_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_users_posts(db, author_id=user_id, skip=skip, limit=limit)
    return posts


