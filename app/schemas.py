from email.policy import default
from lib2to3.pytree import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):    
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    s3_img = Column(LONGTEXT, nullable=False)
    content = Column(LONGTEXT, nullable=False)
    post_datetime = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    message = Column(LONGTEXT, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    msg_datetime = Column(DateTime, nullable=False)

class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)


