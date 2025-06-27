class Author:
    def __init__(self, imie, nazwisko, rok_urodzenia=None, narodowosc=None, id=None):
        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.rok_urodzenia = rok_urodzenia
        self.narodowosc = narodowosc

    def __repr__(self):
        return f"Author({self.id}, {self.imie} {self.nazwisko}, {self.rok_urodzenia}, {self.narodowosc})"

    def full_name(self):
        return f"{self.imie} {self.nazwisko}"


class Book:
    def __init__(self, tytul, autor_id, rok_wydania=None, gatunek=None, liczba_stron=None, opis=None, id=None):
        self.id = id
        self.tytul = tytul
        self.autor_id = autor_id
        self.rok_wydania = rok_wydania
        self.gatunek = gatunek
        self.liczba_stron = liczba_stron
        self.opis = opis

    def __repr__(self):
        return f"Book({self.id}, '{self.tytul}', autor_id={self.autor_id}, {self.rok_wydania}, {self.gatunek}, {self.liczba_stron})"

    def short_description(self):
        return f"'{self.tytul}' ({self.rok_wydania}) - {self.gatunek}"
