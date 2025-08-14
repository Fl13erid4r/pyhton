from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    created = await crud.create_user(db, user)
    if not created:
        raise HTTPException(status_code=400, detail="Email already exists")
    return created

@router.get("/", response_model=List[schemas.UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await crud.list_users(db)
