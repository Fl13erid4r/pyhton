from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from . import models, schemas

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        return None

async def list_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()

async def create_book(db: AsyncSession, book: schemas.BookCreate):
    new_book = models.Book(title=book.title, author=book.author, user_id=book.user_id)
    db.add(new_book)
    try:
        await db.commit()
        await db.refresh(new_book)
        return new_book
    except IntegrityError:
        await db.rollback()
        return None

async def list_books(db: AsyncSession, user_id: int = None):
    query = select(models.Book).where(models.Book.deleted_at.is_(None))
    if user_id:
        query = query.where(models.Book.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()
