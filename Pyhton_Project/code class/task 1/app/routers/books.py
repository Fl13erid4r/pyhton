from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.BookRead)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    created = await crud.create_book(db, book)
    if not created:
        raise HTTPException(status_code=400, detail="Book already exists for this user")
    return created

@router.get("/", response_model=List[schemas.BookRead])
async def list_books(user_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.list_books(db, user_id)
