from pydantic import BaseModel

class BorrowRecord(BaseModel):
    username: str
    book_id: int