# System Zarządzania Budżetem Osobistym

Konsolowa aplikacja w języku Python umożliwiająca śledzenie przychodów i wydatków, generowanie raportów, monitorowanie budżetu i analizowanie nawyków finansowych.

---

##  Funkcje

- Dodawanie, edytowanie i usuwanie transakcji
- Kategorie przychodów i wydatków (możliwość dodawania własnych)
- Filtrowanie i sortowanie transakcji według różnych kryteriów
- Generowanie raportów i statystyk
- Monitorowanie limitów budżetowych wg kategorii
- Eksport danych do pliku CSV
- Prosta wizualizacja danych (wykresy słupkowe – `matplotlib`)
- Dane zapisywane w plikach `.json` — zachowanie historii między uruchomieniami

---

## Wymagania

- Python 3.8+
- Biblioteki:
  - colorama
  - matplotlib
  - pytest
  - sqlalchemy

---

## Instalacja i uruchomienie

1. **Pobierz projekt** (sklonuj repozytorium lub wypakuj plik ZIP).

2. **[Opcjonalnie] Utwórz środowisko wirtualne:**

```bash
python -m venv venv
```

3. **Aktywuj środowisko:**

- Windows:
```bash
venv\Scripts\activate
```

- macOS / Linux:
```bash
source venv/bin/activate
```

4. **Zainstaluj wymagane biblioteki:**

```bash
pip install -r requirements.txt
```

5. **Uruchom aplikację:**

```bash
python main.py
```

---

## Struktura katalogów

```
budget_app/
│   main.py
│   config.json
│   categories.json
│   data.json
│   README.md
│   requirements.txt
│
├── models/              # Klasy: Transaction, TransactionManager
├── storage/             # FileStorage, BaseStorage
├── ui/                  # Interfejs konsolowy
├── reports/             # Raporty, wykresy
├── utils/               # Walidacje, logowanie, config
└── tests/               # Testy jednostkowe
```

---

## Testy

Aby uruchomić testy jednostkowe:

```bash
pytest
```

Testy znajdują się w katalogu `tests/`.

---

## Tryb pracy z bazą danych

Aplikacja wspiera zapis i odczyt z bazy danych SQLite (`DBStorage`) przy użyciu biblioteki `SQLAlchemy`.

- Transakcje są przechowywane w tabeli `transactions.db`.
- Możliwy jest import danych z pliku JSON do bazy danych z poziomu menu (`Opcja 9`).

---

## Autor

Projekt zrealizowany w ramach zaliczenia przedmiotu **"Języki skryptowe – Python"**  
Uniwersytet Gdański, 2025

---

