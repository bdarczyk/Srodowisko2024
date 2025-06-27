import sqlite3
import os
from pathlib import Path

DB_PATH = Path("data/library.db")

def validate_integer(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Wartość musi być większa lub równa {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Wartość musi być mniejsza lub równa {max_val}.")
                continue
            return value
        except ValueError:
            print("Nieprawidłowa wartość. Wprowadź liczbę całkowitą.")

def validate_text(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("To pole nie może być puste.")
        else:
            return value

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True)

        # Poprawiona ścieżka do pliku schema.sql znajdującego się w src/sql/schema.sql
        schema_full_path = Path(__file__).resolve().parent / "schema" / "schema.sql"

        with self.connect() as conn:
            with open(schema_full_path, "r", encoding="utf-8") as schema_file:
                conn.executescript(schema_file.read())
        print("Baza danych została zainicjalizowana zgodnie z schema.sql.")
