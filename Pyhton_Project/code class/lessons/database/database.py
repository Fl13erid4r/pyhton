
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="library",
        user="postgres",
        password="password"
    )

def get_books():
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM books")
                return cursor.fetchall()
    except Exception as e:
        print("Error in get_books:", e)
        return []

def insert_book(title: str, author: str, availablity: bool):
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO books (title, author, availablity) VALUES (%s, %s, %s)",
                    (title, author, availablity)
                )
                conn.commit()
                return {"message": "book added successfully"}
    except Exception as e:
        print("Error in insert_book:", e)
        return {"error": str(e)}

if __name__ == "__main__":
    print("Script started", flush=True)

    books = get_books()

    result = insert_book("Testing", "J.K. Rowling", True)
    print("Insert result:", result)
