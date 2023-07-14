from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship('Post', back_populates='author')

    def __str__(self):
        return f'<User {self.username}>'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='posts')

    def __str__(self):
        return f'<Post {self.title}>'


class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    like = Column(Integer, default=None)
    dislike = Column(Integer, default=None)
