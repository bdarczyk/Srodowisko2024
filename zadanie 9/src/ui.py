from src.repositories import BookRepository, AuthorRepository
from src.models import Book, Author

def menu():
    author_repo = AuthorRepository()
    book_repo = BookRepository()

    while True:
        print("\n--- MENU ---")
        print("1. Dodaj autora")
        print("2. Pokaż wszystkich autorów")
        print("3. Wyszukaj autora po nazwisku")
        print("4. Edytuj autora")
        print("5. Usuń autora")
        print("6. Dodaj książkę")
        print("7. Pokaż wszystkie książki")
        print("8. Wyszukaj książkę")
        print("9. Edytuj książkę")
        print("10. Usuń książkę")
        print("11. Wyświetl książki autora")
        print("12. Zakończ")

        wybor = input("Wybierz opcję: ")

        try:
            if wybor == "1":
                imie = input("Imię: ")
                nazwisko = input("Nazwisko: ")
                rok = int(input("Rok urodzenia: "))
                narodowosc = input("Narodowość: ")
                author_repo.add(Author(imie, nazwisko, rok, narodowosc))
                print("Autor dodany.")

            elif wybor == "2":
                for author in author_repo.get_all():
                    print(author)

            elif wybor == "3":
                nazwisko = input("Nazwisko do wyszukania: ")
                for author in author_repo.find_by_last_name(nazwisko):
                    print(author)

            elif wybor == "4":
                author_id = int(input("ID autora: "))
                imie = input("Nowe imię: ")
                nazwisko = input("Nowe nazwisko: ")
                rok = int(input("Nowy rok urodzenia: "))
                narodowosc = input("Nowa narodowość: ")
                author_repo.update(Author(imie, nazwisko, rok, narodowosc, author_id))
                print("Autor zaktualizowany.")

            elif wybor == "5":
                author_id = int(input("ID autora do usunięcia: "))
                if author_repo.has_books(author_id):
                    print("Nie można usunąć autora przypisanego do książek.")
                else:
                    author_repo.delete(author_id)
                    print("Autor usunięty.")

            elif wybor == "6":
                tytul = input("Tytuł: ")
                autor_id = int(input("ID autora: "))
                rok = int(input("Rok wydania: "))
                gatunek = input("Gatunek: ")
                strony = int(input("Liczba stron: "))
                opis = input("Opis: ")
                book_repo.add(Book(tytul, autor_id, rok, gatunek, strony, opis))
                print("Książka dodana.")

            elif wybor == "7":
                for book in book_repo.get_all():
                    print(book)

            elif wybor == "8":
                query = input("Wpisz tytuł, nazwisko autora lub rok: ")
                for book in book_repo.find(query):
                    print(book)

            elif wybor == "9":
                book_id = int(input("ID książki: "))
                tytul = input("Nowy tytuł: ")
                autor_id = int(input("Nowy ID autora: "))
                rok = int(input("Nowy rok wydania: "))
                gatunek = input("Nowy gatunek: ")
                strony = int(input("Nowa liczba stron: "))
                opis = input("Nowy opis: ")
                book_repo.update(Book(tytul, autor_id, rok, gatunek, strony, opis, book_id))
                print("Książka zaktualizowana.")

            elif wybor == "10":
                book_id = int(input("ID książki do usunięcia: "))
                book_repo.delete(book_id)
                print("Książka usunięta.")

            elif wybor == "11":
                author_id = int(input("ID autora: "))
                books = book_repo.get_by_author(author_id)
                for book in books:
                    print(book)

            elif wybor == "12":
                print("Zamykanie programu...")
                break

            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")

        except Exception as e:
            print(f"Błąd: {e}")