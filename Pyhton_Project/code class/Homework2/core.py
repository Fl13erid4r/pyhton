from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import main
from main import Book, User, lock
from main import UserCreate, UserLogin, BookUpdate
from typing import List
import uvicorn

app = FastAPI()

@app.post("/signup")
def sign_up(user: UserCreate, db: Session = Depends(main.get_db)):
    with lock:
        existing_user = db.query(User).filter(User.name == user.name).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = User(name=user.name, gmail=user.gmail, password=user.password)
        db.add(new_user)
        db.commit()
        return {"message": "User created successfully", "username": user.name}

@app.post("/login")
def log_in(user: UserLogin, db: Session = Depends(main.get_db)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": f"Welcome {user.name}"}

@app.get("/books/available", response_model=List[dict])
def available_books(db: Session = Depends(main.get_db)):
    books = db.query(Book).filter(Book.availablity == True).all()
    return [book.to_dict() for book in books]

@app.post("/books/borrow")
def borrow_book(username: str, book_title: str, db: Session = Depends(main.get_db)):
    with lock:
        book = db.query(Book).filter(Book.title == book_title).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        if not book.availablity or book.copies <= 0:
            raise HTTPException(status_code=400, detail="Book not available or no copies left")

        user = db.query(User).filter(User.name == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        book.copies -= 1
        if book.copies == 0:
            book.availablity = False
        current_borrowed = book.borrowed_by or []
        if username not in current_borrowed:
            current_borrowed.append(username)
        book.borrowed_by = current_borrowed

        user.books_currently_borrowed += 1
        user.total_loans += 1
        current_books = user.books_being_borrowed or []
        if book.title not in current_books:
            current_books.append(book.title)
        user.books_being_borrowed = current_books

        db.commit()
        return {"message": "Book borrowed successfully"}

@app.post("/books/return")
def return_book(username: str, book_title: str, db: Session = Depends(main.get_db)):
    with lock:
        book = db.query(Book).filter(Book.title == book_title).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        current_borrowed = book.borrowed_by or []
        if username not in current_borrowed:
            raise HTTPException(status_code=400, detail="You did not borrow this book")

        book.borrowed_by = [u for u in current_borrowed if u != username]
        book.copies += 1
        if book.copies > 0:
            book.availablity = True

        user = db.query(User).filter(User.name == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.books_currently_borrowed = max(user.books_currently_borrowed - 1, 0)
        current_books = user.books_being_borrowed or []
        user.books_being_borrowed = [b for b in current_books if b != book.title]

        db.commit()
        return {"message": "Book returned successfully"}

@app.get("/users/{username}/loans")
def view_loans(username: str, db: Session = Depends(main.get_db)):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"borrowed_books": user.books_being_borrowed or []}

@app.post("/books/donate")
def donate_book(title: str, author: str, published: int, genre: str, copies: int, db: Session = Depends(main.get_db)):
    with lock:
        book = Book(title=title, author=author, published=published, genre=genre, copies=copies, availablity=True)
        db.add(book)
        db.commit()
        return {"message": "Book donated successfully"}

@app.get("/books/{book_title}")
def book_info(book_title: str, db: Session = Depends(main.get_db)):
    book = db.query(Book).filter(Book.title == book_title).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()

@app.get("/users/{username}")
def user_info(username: str, db: Session = Depends(main.get_db)):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()

@app.put("/users/{username}")
def change_details(username: str, name: str = None, gmail: str = None, password: str = None, original_password: str = None, db: Session = Depends(main.get_db)):
    with lock:
        user = db.query(User).filter(User.name == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if original_password != user.password:
            raise HTTPException(status_code=400, detail="Incorrect original password")
        if name:
            user.name = name
        if gmail:
            user.gmail = gmail
        if password:
            user.password = password
        db.commit()
        return {"message": "User details changed successfully"}


@app.post("/admin/books")
def add_new_book(title: str, author: str, published: int, genre: str, copies: int, db: Session = Depends(main.get_db)):
    with lock:
        book = Book(title=title, author=author, published=published, genre=genre, copies=copies, availablity=True)
        db.add(book)
        db.commit()
        return {"message": "Book added successfully"}


@app.put("/admin/books/{book_title}")
def update_book(book_title: str, book_update: BookUpdate, db: Session = Depends(main.get_db)):
    with lock:
        book = db.query(Book).filter(Book.title == book_title).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = book_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)

        db.commit()
        return {"message": "Book updated successfully"}


@app.delete("/admin/books/{book_title}")
def delete_book(book_title: str, db: Session = Depends(main.get_db)):
    with lock:
        book = db.query(Book).filter(Book.title == book_title).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(book)
        db.commit()
        return {"message": "Book deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)   