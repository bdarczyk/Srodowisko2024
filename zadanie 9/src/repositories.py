import sqlite3
from src.models import Author, Book
from src.database_manager import DB_PATH

class AuthorRepository:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def add(self, author: Author):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO authors (imie, nazwisko, rok_urodzenia, narodowosc)
                VALUES (?, ?, ?, ?)
            """, (author.imie, author.nazwisko, author.rok_urodzenia, author.narodowosc))

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors")
            return [Author(id=row[0], imie=row[1], nazwisko=row[2], rok_urodzenia=row[3], narodowosc=row[4]) for row in cursor.fetchall()]

    def find_by_last_name(self, nazwisko):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE nazwisko LIKE ?", (f"%{nazwisko}%",))
            return [Author(id=row[0], imie=row[1], nazwisko=row[2], rok_urodzenia=row[3], narodowosc=row[4]) for row in cursor.fetchall()]

    def update(self, author: Author):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE authors
                SET imie = ?, nazwisko = ?, rok_urodzenia = ?, narodowosc = ?
                WHERE id = ?
            """, (author.imie, author.nazwisko, author.rok_urodzenia, author.narodowosc, author.id))

    def delete(self, author_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM authors WHERE id = ?", (author_id,))

    def has_books(self, author_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM books WHERE autor_id = ?", (author_id,))
            return cursor.fetchone()[0] > 0


class BookRepository:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def add(self, book: Book):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (tytul, autor_id, rok_wydania, gatunek, liczba_stron, opis)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (book.tytul, book.autor_id, book.rok_wydania, book.gatunek, book.liczba_stron, book.opis))

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            return [Book(id=row[0], tytul=row[1], autor_id=row[2], rok_wydania=row[3], gatunek=row[4], liczba_stron=row[5], opis=row[6]) for row in cursor.fetchall()]

    def find(self, query):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM books
                WHERE tytul LIKE ? OR CAST(rok_wydania AS TEXT) LIKE ?
            """, (f"%{query}%", f"%{query}%"))
            return [Book(id=row[0], tytul=row[1], autor_id=row[2], rok_wydania=row[3], gatunek=row[4], liczba_stron=row[5], opis=row[6]) for row in cursor.fetchall()]

    def update(self, book: Book):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE books
                SET tytul = ?, autor_id = ?, rok_wydania = ?, gatunek = ?, liczba_stron = ?, opis = ?
                WHERE id = ?
            """, (book.tytul, book.autor_id, book.rok_wydania, book.gatunek, book.liczba_stron, book.opis, book.id))

    def delete(self, book_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))

    def get_by_author(self, author_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE autor_id = ?", (author_id,))
            return [Book(id=row[0], tytul=row[1], autor_id=row[2], rok_wydania=row[3], gatunek=row[4], liczba_stron=row[5], opis=row[6]) for row in cursor.fetchall()]