import csv

def borrow_books(books, borrower_name, book_title):
    for book in books:
        if book['title'].lower() == book_title.lower() and str(book['availability']).lower() == 'true':
            book['availability'] = False
            book['borrowed_by'] = borrower_name
            print(f"The book '{book_title}' has been borrowed by {borrower_name}.")
            save_books(books)
            return
    print(f"The book '{book_title}' is not available for borrowing.")

def return_books(books, borrower_name, book_title):
    for book in books:
        if book['title'].lower() == book_title.lower() and book['borrowed_by'].lower() == borrower_name.lower():
            book['availability'] = True
            book['borrowed_by'] = ''
            print(f"The book '{book_title}' has been returned by {borrower_name}.")
            save_books(books)
            return
    print(f"The book '{book_title}' was not borrowed by {borrower_name}.")


def load_books():
    with open('books1.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        books = list(reader)
    return books

def save_books(books):
    with open('books1.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'availability', 'borrowed_by'])
        writer.writeheader()
        for book in books:
            writer.writerow(book)

if __name__ == "__main__":
    sample_books = [
        {'title': 'Harry Potter', 'availability': True, 'borrowed_by': ''},
        {'title': '1984', 'availability': True, 'borrowed_by': ''},
        {'title': 'To Kill a Mockingbird', 'availability': True, 'borrowed_by': ''}
    ]
    save_books(sample_books)
    print("Sample books saved to 'books1.csv'.")
