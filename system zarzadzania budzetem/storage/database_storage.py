from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import csv
import os

from storage.base_storage import BaseStorage
from models.transaction import Transaction

Base = declarative_base()

class TransactionModel(Base):
    """
    Model ORM dla tabeli 'transactions' w SQLite
    mapuje dane z obiektu na rekord SQL.
    Przechowuje dane o kwocie, kategorii, opisie, dacie i typie (income/expense).
    """
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    t_type = Column(String, nullable=False)

class DBStorage(BaseStorage):
    """
    Klasa odpowiedzialna za interakcję z bazą SQLite.
    Implementuje wszystkie metody wymagane przez interfejs BaseStorage.
    """

    def __init__(self, db_path="sqlite:///transactions.db"):
        """
        Inicjalizuje połączenie z bazą danych SQLite.
        Tworzy tabele jeśli nie istnieją.
        """
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine) #tworzy tabele
        self.Session = sessionmaker(bind=self.engine)

    def add_transaction(self, transaction):
        """
        Dodaje nową transakcję do bazy danych.

        transaction: obiekt klasy Transaction
        """
        session = self.Session()
        try:
            new_t = TransactionModel(
                amount=transaction.amount,
                category=transaction.category,
                description=transaction.description,
                date=datetime.strptime(transaction.date, "%Y-%m-%d"),
                t_type=transaction.t_type
            )
            session.add(new_t)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Błąd zapisu do bazy: {e}")
        finally:
            session.close()

    def load(self):
        """
        Ładuje wszystkie transakcje z bazy danych jako listę obiektów Transaction.
        """
        session = self.Session()
        try:
            results = session.query(TransactionModel).all()
            return [
                Transaction(
                    amount=row.amount,
                    category=row.category,
                    description=row.description,
                    date=row.date.strftime("%Y-%m-%d"),
                    t_type=row.t_type
                ) for row in results
            ]
        finally:
            session.close()

    def save(self, transactions):
        """
        Zastępuje wszystkie transakcje w bazie nową listą.

        transactions: lista obiektów Transaction
        """
        session = self.Session()
        try:
            session.query(TransactionModel).delete()
            for t in transactions:
                row = TransactionModel(
                    amount=t.amount,
                    category=t.category,
                    description=t.description,
                    date=datetime.strptime(t.date, "%Y-%m-%d"),
                    t_type=t.t_type
                )
                session.add(row)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Błąd zapisu do bazy: {e}")
        finally:
            session.close()

    def delete_transaction(self, transaction_id):
        """
        Usuwa transakcję o podanym ID.
        transaction_id: int
        """
        session = self.Session()
        try:
            row = session.query(TransactionModel).filter_by(id=transaction_id).first()
            if row:
                session.delete(row)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Błąd podczas usuwania: {e}")
        finally:
            session.close()

    def update_transaction(self, transaction_id, new_data):
        """
        Aktualizuje transakcję na podstawie ID i słownika danych.

        transaction_id: int
        new_data: dict z polami: amount, category, description, date, t_type
        """
        session = self.Session()
        try:
            existing = session.query(TransactionModel).filter_by(id=transaction_id).first()
            if not existing:
                print("Nie znaleziono transakcji.")
                return

            if "amount" in new_data:
                existing.amount = new_data["amount"]
            if "category" in new_data:
                existing.category = new_data["category"]
            if "description" in new_data:
                existing.description = new_data["description"]
            if "date" in new_data:
                existing.date = datetime.strptime(new_data["date"], "%Y-%m-%d")
            if "t_type" in new_data:
                existing.t_type = new_data["t_type"]

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Błąd podczas aktualizacji: {e}")
        finally:
            session.close()

    def export_to_csv(self, transactions, filename="transactions_export.csv"):
        """
        Eksportuje podane transakcje do pliku CSV.

        :param transactions: lista obiektów Transaction
        :param filename: ścieżka do pliku CSV
        """
        try:
            with open(filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
                for t in transactions:
                    writer.writerow([t.date, t.t_type, t.category, t.amount, t.description])
        except Exception as e:
            print(f"Błąd eksportu do CSV: {e}")

    def import_from_json(self, json_path):
        import json
        if not os.path.exists(json_path):
            print(f"Plik {json_path} nie istnieje.")
            return

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            session = self.Session()
            for d in data:
                transaction = TransactionModel(
                    amount=d["amount"],
                    category=d["category"],
                    description=d.get("description", ""),
                    date=datetime.strptime(d["date"], "%Y-%m-%d"),
                    t_type=d["t_type"]
                )
                session.add(transaction)
            session.commit()
            print(f"✔ Zaimportowano {len(data)} transakcji z pliku {json_path}")
        except Exception as e:
            print(f"Błąd podczas importu z JSON: {e}")
