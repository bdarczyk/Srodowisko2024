from models.transaction import Transaction
from utils.validators import is_valid_amount, is_valid_type, is_valid_date
from colorama import Fore, init
from utils.categories import load_categories, add_category
from reports.summary import filter_by_date, summarize, category_breakdown, plot_breakdown
from datetime import datetime
from utils.config import load_config, update_budget_limit
from collections import defaultdict

init(autoreset=True)

def show_menu(manager, config):
    """
    Wyświetla główne menu aplikacji i obsługuje wszystkie interakcje z użytkownikiem.

    Funkcja umożliwia:
    1. Dodawanie nowych transakcji (z walidacją, wyborem typu i kategorii)
    2. Przeglądanie transakcji z filtrowaniem i sortowaniem
    3. Obliczanie bilansu finansowego
    4. Eksport danych do pliku CSV
    5. Generowanie raportu z wybranego okresu (łącznie z wykresem słupkowym)
    6. Monitorowanie miesięcznego budżetu kategorii
    7. Usuwanie transakcji z potwierdzeniem
    8. Edytowanie transakcji (dowolnych pól)
    0. Zakończenie programu

    manager Obiekt klasy TransactionManager – zarządza listą transakcji
    config  Słownik konfiguracji wczytany z pliku config.json
    """
    currency = config.get("default_currency", "zł")
    while True:
        print(Fore.CYAN + "\n=== Budżet Osobisty ===")
        print("1. Dodaj transakcję")
        print("2. Wyświetl wszystkie transakcje")
        print("3. Pokaż bilans")
        print("4. Eksportuj transakcje do CSV")
        print("5. Generuj raport")
        print("6. Monitoruj budżet")
        print("7. Usuń transakcję")
        print("8. Edytuj transakcję")
        print("9. Importuj dane z pliku JSON do bazy")
        print("0. Wyjście")
        choice = input("Wybierz opcję: ")

        if choice == "1":
            amount = input("Kwota: ")
            if not is_valid_amount(amount):
                print(Fore.RED + "❌ Niepoprawna kwota. Użyj np. 123.45")
                continue

            description = input("Opis: ")

            date = input("Data (YYYY-MM-DD): ")
            if not is_valid_date(date):
                print(Fore.RED + "❌ Niepoprawna data. Użyj np. 2025-06-15")
                continue

            t_type = input("Typ (income/expense): ").lower()
            if not is_valid_type(t_type):
                print(Fore.RED + "❌ Niepoprawny typ. Użyj: income lub expense")
                continue

            categories_file = config.get("categories_file", "categories.json")
            categories = load_categories(categories_file)

            print("Dostępne kategorie:")
            for idx, cat in enumerate(categories[t_type]):
                print(f"{idx + 1}. {cat}")
            print("0. Dodaj nową kategorię")

            choice_cat = input("Wybierz kategorię (numer lub 0): ")
            if choice_cat == "0":
                new_cat = input("Podaj nazwę nowej kategorii: ")
                add_category(t_type, new_cat, categories_file)
                category = new_cat
            elif choice_cat.isdigit() and 1 <= int(choice_cat) <= len(categories[t_type]):
                category = categories[t_type][int(choice_cat) - 1]
            else:
                print(Fore.RED + "❌ Niepoprawny wybór kategorii.")
                continue
            transaction = Transaction(amount, category, description, date, t_type=t_type)
            manager.add_transaction(transaction)
            print(Fore.GREEN + "✔ Transakcja dodana.")

        elif choice == "2":
            all_transactions = manager.list_transactions()
            if not all_transactions:
                print(Fore.YELLOW + "Brak transakcji do wyświetlenia.")
                continue
            print(Fore.CYAN + "\n--- Podmenu: przeglądanie transakcji ---")
            print("1. Wyświetl wszystkie")
            print("2. Filtrowanie")
            print("3. Sortowanie")
            print("4. Filtrowanie + sortowanie")
            print("0. Powrót")
            sub_choice = input("Wybierz opcję: ")
            transactions = all_transactions
            if sub_choice == "2" or sub_choice == "4":
                filter_cat = input("Filtruj po kategorii (Enter = brak): ").strip()
                filter_type = input("Filtruj po typie (income/expense/Enter): ").strip().lower()
                min_amount = input("Minimalna kwota (Enter = brak): ").strip()
                max_amount = input("Maksymalna kwota (Enter = brak): ").strip()
                if filter_cat:
                    transactions = list(filter(lambda t: t.category.lower() == filter_cat.lower(), transactions)) # filtruje listę transakcji.
                if filter_type in ["income", "expense"]:
                    transactions = list(filter(lambda t: t.t_type == filter_type, transactions))
                if min_amount:
                    try:
                        min_val = float(min_amount)
                        transactions = list(filter(lambda t: t.amount >= min_val, transactions))
                    except ValueError:
                        print(Fore.RED + "❌ Niepoprawna minimalna kwota.")
                        continue
                if max_amount:
                    try:
                        max_val = float(max_amount)
                        transactions = list(filter(lambda t: t.amount <= max_val, transactions))
                    except ValueError:
                        print(Fore.RED + "❌ Niepoprawna maksymalna kwota.")
                        continue
            if sub_choice == "3" or sub_choice == "4":
                print("Sortuj wg:")
                print("1. Data")
                print("2. Kwota")
                print("3. Kategoria")
                sort_choice = input("Wybierz: ").strip()
                if sort_choice == "1":
                    transactions.sort(key=lambda t: t.date)
                elif sort_choice == "2":
                    transactions.sort(key=lambda t: t.amount)
                elif sort_choice == "3":
                    transactions.sort(key=lambda t: t.category.lower())

            if sub_choice == "0":
                continue
            print(Fore.CYAN + "\n--- Wynik ---")
            if not transactions:
                print(Fore.YELLOW + "Brak pasujących transakcji.")
            else:
                for t in transactions:
                    print(f"{t.date} | {t.t_type.upper():<7} | {t.category:<10} | {t.amount:.2f} {currency} | {t.description}")


        elif choice == "3":
            balance = manager.get_balance()
            print(Fore.YELLOW + f"Aktualny bilans: {balance:.2f} {currency}")

        elif choice == "4":
            export_file = config.get("export_file", "transactions_export.csv")
            manager.storage.export_to_csv(manager.list_transactions(), filename=export_file)
            print(Fore.GREEN + f"✔ Eksport zakończony. Plik: {export_file}")

        elif choice == "5":

            start = input("Data początkowa (YYYY-MM-DD): ").strip()
            end = input("Data końcowa (YYYY-MM-DD): ").strip()

            try:
                datetime.strptime(start, "%Y-%m-%d")
                datetime.strptime(end, "%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "❌ Niepoprawny format daty.")
                continue

            data = filter_by_date(manager.list_transactions(), start, end)
            if not data:
                print(Fore.YELLOW + "Brak transakcji w podanym okresie.")
                continue

            income, expenses, balance, avg, max_val, min_val = summarize(data)

            print(Fore.CYAN + "\n--- Raport finansowy ---")
            print(f"Przychody:     {income:.2f} {currency}")
            print(f"Wydatki:       {expenses:.2f} {currency}")
            print(f"Bilans:        {balance:.2f} {currency}")
            print(f"Średnia wartość transakcji: {avg:.2f} {currency}")
            print(f"Największa:    {max_val:.2f} {currency}")
            print(f"Najmniejsza:   {min_val:.2f} {currency}")

            breakdown = category_breakdown(data)
            if breakdown:
                print(Fore.CYAN + "\n--- Wydatki wg kategorii ---")
                for cat, (amt, percent) in breakdown.items():
                    print(f"{cat:<15} {amt:>8.2f} {currency}  ({percent:.2f}%)")
                plot_breakdown(breakdown)


        elif choice == "6":
            while True:
                print(Fore.CYAN + "\n--- Monitor budżetu ---")
                print("1. Wyświetl stan budżetu")
                print("2. Ustaw / zmień limit dla kategorii")
                print("0. Powrót")
                sub_choice = input("Wybierz opcję: ").strip()
                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    config = load_config()
                    budgets = config.get("budgets", {})

                    transactions = manager.list_transactions()
                    expense_summary = defaultdict(float)

                    for t in transactions:
                        if t.t_type == "expense":
                            try:
                                date = datetime.strptime(t.date, "%Y-%m-%d")
                                if date.year == 2025 and date.month == 6:
                                    expense_summary[t.category] += t.amount
                            except:
                                continue

                    print(Fore.CYAN + "\n--- Monitor budżetu (Czerwiec 2025) ---")
                    print(f"{'Kategoria':<20} {'Limit':>10} {'Wydano':>10} {'Pozostało':>12} Status")
                    print("-" * 60)
                    for category, limit in budgets.items():
                        spent = expense_summary.get(category, 0.0)
                        remaining = round(limit - spent, 2)
                        status = "✅ OK" if remaining >= 0 else "❌ PRZEKROCZONO"
                        print(f"{category:<20} {limit:>10.2f} {spent:>10.2f} {remaining:>12.2f} {status}")
                    pass
                elif sub_choice == "2":
                    categories = load_categories()
                    all_cats = categories["expense"]  # limity mają sens tylko dla wydatków
                    print("Dostępne kategorie wydatków:")
                    for idx, cat in enumerate(all_cats):
                        print(f"{idx + 1}. {cat}")
                    try:
                        idx = int(input("Wybierz kategorię: ")) - 1
                        selected = all_cats[idx]
                        new_limit = float(input(f"Nowy limit dla '{selected}': "))
                        update_budget_limit(selected, new_limit)
                        print(Fore.GREEN + f"✔ Limit zaktualizowany: {selected} → {new_limit:.2f} {currency}")
                    except Exception as e:
                        print(Fore.RED + f"❌ Błąd: {e}")


        elif choice == "7":
            transactions = manager.list_transactions()

            if not transactions:
                print(Fore.YELLOW + "Brak transakcji do usunięcia.")
                continue

            print(Fore.CYAN + "\n--- Lista transakcji ---")
            for idx, t in enumerate(transactions):
                print(
                    f"{idx + 1}. {t.date} | {t.t_type.upper():<7} | {t.category:<10} | {t.amount:.2f} {currency} | {t.description}")

            try:
                to_delete = int(input("Podaj numer transakcji do usunięcia: "))
                if 1 <= to_delete <= len(transactions):
                    confirm = input("Czy na pewno chcesz usunąć tę transakcję? (t/n): ").lower()
                    if confirm == "t":
                        removed = manager.delete_transaction_by_index(to_delete - 1)
                        manager.save()  # zapisanie do pliku
                        print(
                            Fore.GREEN + f"✔ Usunięto: {removed.category} | {removed.amount:.2f} {currency} | {removed.description}")
                    else:
                        print(Fore.YELLOW + "❕ Anulowano usuwanie.")
                else:
                    print(Fore.RED + "❌ Nieprawidłowy numer.")
            except ValueError:
                print(Fore.RED + "❌ Wprowadź poprawny numer.")


        elif choice == "8":
            transactions = manager.list_transactions()
            if not transactions:
                print(Fore.YELLOW + "Brak transakcji do edycji.")
                continue

            print(Fore.CYAN + "\n--- Lista transakcji ---")
            for idx, t in enumerate(transactions):
                print(
                    f"{idx + 1}. {t.date} | {t.t_type.upper():<7} | {t.category:<10} | {t.amount:.2f} {currency} | {t.description}")

            try:
                i = int(input("Wybierz numer transakcji do edycji: ")) - 1
                if i < 0 or i >= len(transactions):
                    print(Fore.RED + "❌ Nieprawidłowy numer.")
                    continue
                t = transactions[i]

                print(Fore.YELLOW + "\n--- Wprowadź nowe dane (Enter = bez zmian) ---")
                new_amount = input(f"Kwota [{t.amount}]: ").strip()
                new_cat = input(f"Kategoria [{t.category}]: ").strip()
                new_desc = input(f"Opis [{t.description}]: ").strip()
                new_date = input(f"Data [{t.date}]: ").strip()
                new_type = input(f"Typ (income/expense) [{t.t_type}]: ").strip().lower()

                new_data = {}

                if new_amount:
                    if is_valid_amount(new_amount):
                        new_data["amount"] = float(new_amount)
                    else:
                        print(Fore.RED + "❌ Niepoprawna kwota.")
                        continue
                if new_cat:
                    new_data["category"] = new_cat
                if new_desc:
                    new_data["description"] = new_desc
                if new_date:
                    if is_valid_date(new_date):
                        new_data["date"] = new_date
                    else:
                        print(Fore.RED + "❌ Niepoprawna data.")
                        continue
                if new_type in ["income", "expense"]:
                    new_data["t_type"] = new_type
                elif new_type:
                    print(Fore.RED + "❌ Niepoprawny typ.")
                    continue

                if manager.update_transaction_by_index(i, new_data):
                    print(Fore.GREEN + "✔ Transakcja zaktualizowana.")
                else:
                    print(Fore.RED + "❌ Błąd aktualizacji.")

            except ValueError:
                print(Fore.RED + "❌ Błąd: wpisz poprawny numer.")

        elif choice == "9":
            json_path = input("Podaj ścieżkę do pliku JSON (np. data.json): ").strip()
            if hasattr(manager.storage, "import_from_json"):
                manager.storage.import_from_json(json_path)
                manager.transactions = manager.storage.load()
                print(Fore.GREEN + "✔ Import zakończony.")
            else:
                print(Fore.RED + "❌ Wybrany system przechowywania nie obsługuje importu.")
        elif choice == "0":
            print("Zamykam program.")
            break
        else:
            print(Fore.RED + "Nieznana opcja.")
