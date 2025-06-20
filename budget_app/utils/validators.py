import re

def is_valid_amount(amount):
    """
    Sprawdza, czy podana kwota jest poprawna (liczba dziesiętna z maks. 2 miejscami po przecinku).

    amount Kwota w formacie tekstowym (np. "123.45")
    return True jeśli poprawna, False w przeciwnym razie
    """
    return re.match(r"^\d+(\.\d{1,2})?$", amount) is not None

def is_valid_date(date):
    """
    Sprawdza, czy podana data jest w formacie RRRR-MM-DD.

    param date Data w formacie tekstowym (np. "2025-06-19")
    return True jeśli poprawna, False w przeciwnym razie
    """
    return re.match(r"^\d{4}-\d{2}-\d{2}$", date) is not None

def is_valid_type(t_type):
    """
    Sprawdza, czy typ transakcji jest jednym z dozwolonych: "income" lub "expense".

    param t_type Typ transakcji w formacie tekstowym
    return True jeśli poprawny, False w przeciwnym razie
    """
    return t_type.lower() in ["income", "expense"]