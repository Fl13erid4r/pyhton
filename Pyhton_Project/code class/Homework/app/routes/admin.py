from fastapi import APIRouter, HTTPException, Depends
from app.schemas.book_schema import BookOut, DonateIn
from app.api.dependencies import get_admin_user
from core.business_logic import donate_book, list_books

router = APIRouter()

@router.post("/donate", response_model=BookOut, summary="Admin donate/add book")
def admin_donate(req: DonateIn, admin: str = Depends(get_admin_user)):
    book = donate_book(req.title, req.author)
    return book

@router.get("/books", response_model=list[BookOut], summary="Admin list books")
def admin_list(admin: str = Depends(get_admin_user)):
    return list_books()