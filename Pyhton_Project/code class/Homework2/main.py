from sqlalchemy import create_engine, Column, Integer, Boolean, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import threading

DATABASE_URL = "postgresql://postgres:password@localhost:5432/library"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

lock = threading.Lock() 

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    availablity = Column(Boolean, default=True)  
    published = Column(Integer)
    genre = Column(String)
    borrowed_by = Column(JSON, default=list)
    copies = Column(Integer, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published": self.published,
            "genre": self.genre,
            "borrowed_by": self.borrowed_by,
            "availablity": self.availablity,
            "copies": self.copies
        }

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gmail = Column(String, index=True)
    password = Column(String, index=True)
    books_currently_borrowed = Column(Integer, default=0)
    total_loans = Column(Integer, default=0)
    books_being_borrowed = Column(JSON, default=list)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gmail": self.gmail,
            "password": self.password,
            "number_of_books_currently_borrowed": self.books_currently_borrowed,
            "number_of_total_loans": self.total_loans,
            "books_being_borrowed": self.books_being_borrowed
        }

Base.metadata.create_all(bind=engine)

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    gmail: str
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published: Optional[int]
    genre: Optional[str]
    copies: Optional[int]
    availablity: Optional[bool]
    borrowed_by: Optional[List[str]]