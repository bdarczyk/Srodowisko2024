-- Tworzenie tabeli autorów
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    rok_urodzenia INTEGER,
    narodowosc TEXT
);

-- Tworzenie tabeli książek
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tytul TEXT NOT NULL,
    autor_id INTEGER,
    rok_wydania INTEGER,
    gatunek TEXT,
    liczba_stron INTEGER,
    opis TEXT,
    FOREIGN KEY (autor_id) REFERENCES authors (id)
);
