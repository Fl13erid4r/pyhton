# library_management

import csv

def load_books():
    with open('books.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        books = list(reader)    
        for book in books:
            book['availability'] = book['availability'].strip().lower() == 'true'
            book['published_year'] = int(book['published_year'])
    return books

def save_books(books):
    with open('books.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'availability', 'borrowed_by' ,'author',"published_year",'genre'])
        writer.writeheader()
        for book in books:
            book_copy = book.copy()
            book_copy['availability'] = 'True' if book_copy['availability'] else 'False'
            book_copy['published_year'] = str(book_copy['published_year'])
            writer.writerow(book_copy)

def getcsv():
    data = [
        {'title': 'harry potter', 'availability': True, 'borrowed_by': '', 'author': 'J.K.Rowling', 'published_year': 1997, 'genre': 'Fantasy'},
        {'title': '1984', 'availability': False, 'borrowed_by': 'Rutwik', 'author': 'George Orwell', 'published_year': 1949, 'genre': 'Dystopian'},
        {'title': 'to kill a mockingbird', 'availability': True, 'borrowed_by': '', 'author': 'Harper Lee', 'published_year': 1960, 'genre': 'Thriller'},
    ]
    save_books(data)

#getcsv()
#load_books()
