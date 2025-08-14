import threading
from defs import save_books,load_books,borrow_books


books = load_books()

t1 = threading.Thread(target=borrow_books, args=(books, "Amy", "Harry Potter"))
t2 = threading.Thread(target=borrow_books, args=(books, "Bob", "1984"))

t1.start()
t2.start()
t1.join()
t2.join()

print("Final book states:")
for book in books:
    print(book)
