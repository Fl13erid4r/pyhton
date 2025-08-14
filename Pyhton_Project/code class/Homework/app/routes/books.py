from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from app.schemas.book_schema import BookOut, BorrowIn, ReturnIn, DonateIn, SimulateIn
from app.api.dependencies import get_current_user_optional
from core.business_logic import (
    list_books, borrow_book, return_book, donate_book, query_user_borrowed, simulate_concurrent_actions
)

router = APIRouter()

@router.get("/", response_model=List[BookOut], summary="List all books")
def get_books():
    return list_books()

@router.post("/borrow", summary="Borrow a book")
def post_borrow(req: BorrowIn, user: str = Depends(get_current_user_optional)):
    username = req.username or user
    if not username:
        raise HTTPException(status_code=400, detail="username required")
    ok, msg = borrow_book(username, req.book_id)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.post("/return", summary="Return a book")
def post_return(req: ReturnIn, user: str = Depends(get_current_user_optional)):
    username = req.username or user
    if not username:
        raise HTTPException(status_code=400, detail="username required")
    ok, msg = return_book(username, req.book_id)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.post("/donate", summary="Donate a book")
def post_donate(req: DonateIn):
    book = donate_book(req.title, req.author)
    return book

@router.post("/simulate", summary="Start a simulation of concurrent users")
def post_simulate(req: SimulateIn, background_tasks: BackgroundTasks):
    # schedule background simulation using FastAPI background tasks
    background_tasks.add_task(simulate_concurrent_actions, req.actions)
    return {"message": "simulation started"}

@router.get("/user/{username}", response_model=List[BookOut], summary="Get all books borrowed by a user")
def get_user_books(username: str):
    return query_user_borrowed(username)