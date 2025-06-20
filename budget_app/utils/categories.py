import json
import os

CATEGORIES_FILE = "categories.json"

def load_categories(path=CATEGORIES_FILE):
    """
    Wczytuje słownik kategorii z pliku JSON.

    path: Ścieżka do pliku z kategoriami (domyślnie 'categories.json')
    return Słownik z kategoriami: income, expense
    """
    if not os.path.exists(path):
        return {"income": [], "expense": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_categories(categories, path=CATEGORIES_FILE):
    """
    Zapisuje słownik kategorii do pliku JSON.

    categories Słownik income: ... , expense: ....
    path Ścieżka do pliku zapisu (domyślnie 'categories.json')
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4, ensure_ascii=False)

def add_category(category_type, name, path=CATEGORIES_FILE):
    """
    Dodaje nową kategorię do wybranego typu ('income' lub 'expense').

    category_type Typ kategorii ('income' lub 'expense')
    name Nazwa nowej kategorii
    path Ścieżka do pliku kategorii (domyślnie 'categories.json')
    """
    categories = load_categories(path)
    if name not in categories[category_type]:
        categories[category_type].append(name)
        save_categories(categories, path)
