from fastapi import FastAPI,HTTPException,Request
from Library import save_books,load_books
import uvicorn
import csv
from pydantic import BaseModel
app = FastAPI()

class Book(BaseModel):
    title: str
    availability: bool
    borrowed_by: str
    author: str
    published_year: int
    genre: str

class Borrow_Request(BaseModel):
    title: str
    name: str

class ReturnRequest(BaseModel):
    name: str
    title: str

class DonateRequest(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str
    

@app.get('/books/available')
def view_available_books():
    books = load_books()
    return [book['title'] for book in books if str(book['availability']).lower() == 'true']

@app.post('/books/borrow/')
def borrow_books(request : Borrow_Request):
    books = load_books()
    for book in books:
        if book['title'].lower() == request.title.lower() and str(book['availability']).lower() == 'true':
            book['availability'] = False
            book['borrowed_by'] = request.name
            save_books(books)
            return {"message": "The book has been borrowed."}
    return{"message" : "The book is not available"}


@app.get("/books/borrowed/{name}")
def view_borrowed_books(name: str):
    books = load_books()
    return [book['title'] for book in books if book['borrowed_by'].lower() == name.lower()]

@app.post("/books/return")
def return_book(request: ReturnRequest):
    books = load_books()
    for book in books:
        if book['title'].lower() == request.title.lower() and book['borrowed_by'].lower() == request.name.lower():
            book['availability'] = True
            book['borrowed_by'] = ""
            save_books(books)
            return {"message": "Book returned successfully."}
    return {"message": "Book not found or not borrowed by you."}


@app.post("/books/donate")
def donate_book(book: DonateRequest):
    books = load_books()
    new_book = {
        'title': book.title,
        'availability': True,
        'borrowed_by': '',
        'author': book.author,
        'published_year': book.published_year,
        'genre': book.genre
    }
    books.append(new_book)
    save_books(books)
    return {"message": f"Thank you for donating {book.title}!"}

@app.get("/books/info/{title}")
def view_book_info(title: str):
    books = load_books()
    for book in books:
        if book['title'].lower() == title.lower():
            return book
    return{"message":"The book can be found"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)   
