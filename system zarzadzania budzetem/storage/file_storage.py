"""
Obsługa plików: FileStorage
Zapis i odczyt danych z/do plików JSON i CSV.
"""

import os
import json
import csv
from models.transaction import Transaction
from storage.base_storage import BaseStorage

class FileStorage(BaseStorage):
    """
    Klasa odpowiedzialna za zapisywanie i wczytywanie transakcji z plików.
    Implementuje zapis do pliku JSON oraz eksport do CSV.
    """
    def __init__(self, filename="data.json"):
        """
        Inicjalizuje obiekt FileStorage z domyślną nazwą pliku.
        """
        self._filename = filename  # ← ENKAPSULACJA
    @property
    def filename(self):
        """
        Getter — pozwala odczytać nazwę pliku w bezpieczny sposób.
        """
        return self._filename


    def load(self):
        """
        Wczytuje dane z pliku JSON. Zwraca listę obiektów Transaction.
        zwraca liste Transaction lub pustą liste przy błędzie
        """
        try:
            if not os.path.exists(self.filename):
                return []
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Transaction.from_dict(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Błąd odczytu pliku {self.filename}: {e}")
            return []

    def save(self, transactions):
        """
        Zapisuje listę transakcji do pliku JSON.
        """
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in transactions], f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Błąd zapisu do pliku {self.filename}: {e}")

    def export_to_csv(self, transactions, filename="transactions_export.csv"):
        """
        Eksportuje listę transakcji do pliku CSV.

        transactions: lista obiektów Transaction
        filename: nazwa pliku CSV (domyślnie 'transactions_export.csv')
        """
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
            for t in transactions:
                writer.writerow([t.date, t.t_type, t.category, t.amount, t.description])
