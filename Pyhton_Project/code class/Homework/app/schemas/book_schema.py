from pydantic import BaseModel
from typing import Optional

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    available: bool

class DonateIn(BaseModel):
    title: str
    author: str

class BorrowIn(BaseModel):
    username: Optional[str] = None
    book_id: int

class ReturnIn(BaseModel):
    username: Optional[str] = None
    book_id: int

class SimulateAction(BaseModel):
    username: str
    action: str  # 'borrow' or 'return'
    book_id: int

class SimulateIn(BaseModel):
    actions: list[SimulateAction]