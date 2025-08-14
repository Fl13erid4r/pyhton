-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     Name VARCHAR(255) NOT NULL,
--     Gmail VARCHAR(255) UNIQUE NOT NULL,
--     Books_Currently_Borrowed INTEGER DEFAULT 0,
--     Total_Loans INTEGER DEFAULT 0,
--     Books_Being_Borrowed TEXT[]  -- array of book titles
-- );

-- CREATE TABLE books (
--     id SERIAL PRIMARY KEY,
--     Title VARCHAR(255) NOT NULL,
--     Availablity BOOlEAN DEFAULT TRUE ,
--     Copies INTEGER NOT NULL,
--     Borrowed_By TEXT[] ,
--     Author VARCHAR(255),
--     Published INTEGER,
--     Genre VARCHAR(255)
-- );

-- INSERT INTO books (Title, Availablity, Copies, Author, Published, Genre)
-- VALUES 
-- ('The Great Gatsby', TRUE, 5, 'F. Scott Fitzgerald', 1925, 'Fiction'),
-- ('To Kill a Mockingbird', TRUE, 3, 'Harper Lee', 1960, 'Fiction'),
-- ('1984', TRUE, 2, 'George Orwell', 1949, 'Dystopian'),
-- ('Harry Potter and the Sorcerer''s Stone', TRUE, 4, 'J.K. Rowling', 1997, 'Fantasy'),
-- ('Pride and Prejudice', TRUE, 6, 'Jane Austen', 1813, 'Romance'),
-- ('The Hobbit', TRUE, 3, 'J.R.R. Tolkien', 1937, 'Fantasy'),
-- ('The Lord of the Rings', TRUE, 2, 'J.R.R. Tolkien', 1954, 'Fantasy')
-- ;

ALTER TABLE users
ADD COLUMN Password VARCHAR(255);

INSERT INTO users (Name, Gmail, Password)
VALUES ('Admin', 'admin@gmail.com', '123456');

