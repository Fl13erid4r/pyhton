from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    books = relationship("Book", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    author = Column(Text)
    added_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="books")

    __table_args__ = (UniqueConstraint("user_id", "title", name="uq_user_book_title"),)
