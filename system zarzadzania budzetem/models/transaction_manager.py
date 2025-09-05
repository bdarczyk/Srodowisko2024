"""
TransactionManager – zarządza logiką dodawania, edytowania, usuwania i pobierania transakcji.
Działa z różnymi systemami przechowywania danych (np. FileStorage, DBStorage).
"""
class TransactionManager:
    """
    Klasa zarządzająca listą transakcji i komunikacją ze storage (plikowym lub bazodanowym).
    """

    def __init__(self, storage):
        """
        Inicjalizuje menedżera z wybraną implementacją storage.

        storage: instancja klasy dziedziczącej po BaseStorage
        """
        self.storage = storage
        self.transactions = self.storage.load()

    def add_transaction(self, transaction):
        """
        Dodaje nową transakcję i zapisuje dane.

        transaction: obiekt klasy Transaction
        """
        self.transactions.append(transaction)
        if hasattr(self.storage, "add_transaction"):
            self.storage.add_transaction(transaction)
        else:
            self.storage.save(self.transactions)

    def list_transactions(self):
        """
        Zwraca listę wszystkich transakcji.
        """
        return self.transactions

    def get_balance(self):
        """
        Oblicza bilans: suma przychodów minus suma wydatków.
        """
        income = sum(t.amount for t in self.transactions if t.t_type == "income")
        expense = sum(t.amount for t in self.transactions if t.t_type == "expense")
        return round(income - expense, 2)

    def delete_transaction_by_index(self, index):
        """
        Usuwa transakcję z listy i ze storage.

        index: indeks na liście transactions
        """
        if 0 <= index < len(self.transactions):
            removed = self.transactions.pop(index)
            if hasattr(self.storage, "save"):
                self.storage.save(self.transactions)
            elif hasattr(self.storage, "delete_transaction"):
                self.storage.delete_transaction(index + 1)
            return removed
        return None

    def update_transaction_by_index(self, index, new_data):
        """
        Aktualizuje transakcję na wskazanym indeksie danymi z new_data.

        index: indeks na liście
        new_data: słownik z nowymi wartościami pól
        """
        if 0 <= index < len(self.transactions):
            t = self.transactions[index]
            for key, value in new_data.items():
                if hasattr(t, key):
                    setattr(t, key, value)

            if hasattr(self.storage, "update_transaction"):
                self.storage.update_transaction(index + 1, new_data)
            elif hasattr(self.storage, "save"):
                self.storage.save(self.transactions)
            return True
        return False

    def save(self):
        """
        Wymusza zapis transakcji (gdy storage nie zapisuje automatycznie).
        """
        if hasattr(self.storage, "save"):
            self.storage.save(self.transactions)
