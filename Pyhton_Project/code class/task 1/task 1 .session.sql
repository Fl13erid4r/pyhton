DROP TABLE users;
DROP TABLE books;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    added_at TIMESTAMPTZ DEFAULT NOW(),
    user_id INT REFERENCES users(id),
    CONSTRAINT uq_user_book_title UNIQUE (user_id, title)
);


INSERT INTO users (name, email) VALUES
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com');

--Alice
INSERT INTO books (title, author, user_id) VALUES
('1984', 'George Orwell', 1),
('Animal Farm', 'George Orwell', 1),
('Pride and Prejudice', 'Jane Austen', 1),
('The Great Gatsby', 'F. Scott Fitzgerald', 1),
('Moby Dick', 'Herman Melville', 1);

-- Bob
INSERT INTO books (title, author, user_id) VALUES
('Dune', 'Frank Herbert', 2),
('Foundation', 'Isaac Asimov', 2),
('The Catcher in the Rye', 'J.D. Salinger', 2),
('To Kill a Mockingbird', 'Harper Lee', 2),
('Brave New World', 'Aldous Huxley', 2);

