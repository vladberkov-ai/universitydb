PRAGMA foreign_keys = ON;
CREATE TABLE Readers (reader_id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(trim(name))>0)) STRICT;
CREATE TABLE Books (book_id INTEGER PRIMARY KEY, title TEXT NOT NULL CHECK(length(trim(title))>0)) STRICT;
CREATE TABLE Loans (loan_id INTEGER PRIMARY KEY, reader_id INTEGER NOT NULL REFERENCES Readers, book_id INTEGER NOT NULL REFERENCES Books, returned INTEGER NOT NULL CHECK(returned IN (0,1))) STRICT;
