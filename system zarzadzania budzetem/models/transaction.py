"""
Model danych: Transaction
Reprezentuje pojedynczą transakcję budżetową.
"""

from datetime import datetime

class Transaction:
    """
    Klasa reprezentująca transakcję (przychód lub wydatek).
    """
    def __init__(self, amount, category, description, date=None, t_type="expense"):
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')
        self.t_type = t_type  # 'income' or 'expense'
        """
        Inicjalizuje nową transakcję.

        amount: Kwota transakcji (float)
        category: Kategoria transakcji (str)
        description: Opis transakcji (str)
        date: Data transakcji (str, format YYYY-MM-DD, opcjonalnie)
        t_type: Typ transakcji: "income" lub "expense"
        """


    def to_dict(self):
        """
        Konwertuje obiekt transakcji do słownika (do zapisu w JSON).
        """
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "t_type": self.t_type
        }

    @staticmethod
    def from_dict(data):
        """
        Tworzy obiekt Transaction na podstawie danych ze słownika (np. z JSON-a).
        data: dict z kluczami: amount, category, description, date, t_type
        return Transaction
        """
        return Transaction(
            data["amount"],
            data["category"],
            data["description"],
            data["date"],
            data["t_type"]
        )
