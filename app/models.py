from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship

from app.database import Base


posts_likes = Table(
    "posts_likes",
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
)


posts_dislikes = Table(
    "posts_dislikes",
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    location = Column(String)

    posts = relationship('Post', back_populates='author')
    likes_posts = relationship('Post', secondary="posts_likes", back_populates='whom_likes')
    dislikes_posts = relationship('Post', secondary="posts_dislikes", back_populates='whom_dislikes')

    def __str__(self):
        return f'<User {self.username}>'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='posts')
    whom_likes = relationship('User', secondary="posts_likes", back_populates='likes_posts')
    whom_dislikes = relationship('User', secondary="posts_dislikes", back_populates='dislikes_posts')

    def __str__(self):
        return f'<Post {self.title}>'

    @property
    def likes(self):
        return len(self.whom_likes)

    @property
    def dislikes(self):
        return len(self.whom_dislikes)

