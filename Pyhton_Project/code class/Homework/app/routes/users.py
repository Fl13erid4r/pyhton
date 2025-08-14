from fastapi import APIRouter, Depends
from typing import List
from app.schemas.user_schema import UserBorrowedOut
from app.api.dependencies import get_current_user
from core.business_logic import query_user_borrowed

router = APIRouter()

@router.get("/me/borrowed", response_model=List[UserBorrowedOut], summary="Get my borrowed books")
def get_my_borrowed(user: str = Depends(get_current_user)):
    books = query_user_borrowed(user)
    return books