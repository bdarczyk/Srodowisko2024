import matplotlib.pyplot as plt
from collections import defaultdict

def filter_by_date(transactions, start_date, end_date):
    """
    Filtruje transakcje, zwracając tylko te mieszczące się w podanym zakresie dat.

    transactions Lista obiektów Transaction
    start_date Data początkowa
    end_date Data końcowa
    return: Lista przefiltrowanych transakcji
    """
    return [
        t for t in transactions
        if start_date <= t.date <= end_date
    ]

def summarize(transactions):
    """
    Oblicza podsumowanie transakcji: przychody, wydatki, bilans,
    średnia, największa i najmniejsza kwota.

    transactions Lista obiektów Transaction
    return tuple (income, expenses, balance, avg, max, min)
    """
    income = sum(t.amount for t in transactions if t.t_type == "income")
    expenses = sum(t.amount for t in transactions if t.t_type == "expense")
    balance = income - expenses

    amounts = [t.amount for t in transactions]
    if amounts:
        avg = sum(amounts) / len(amounts)
        max_val = max(amounts)
        min_val = min(amounts)
    else:
        avg = max_val = min_val = 0

    return income, expenses, balance, avg, max_val, min_val

def category_breakdown(transactions):
    """
    Generuje podsumowanie wydatków wg kategorii oraz ich procentowego udziału.

    transactions: Lista obiektów Transaction
    return Słownik: {kategoria: (kwota, procent)}
    """
    totals = defaultdict(float)
    for t in transactions:
        if t.t_type == "expense":
            totals[t.category] += t.amount
    total_expenses = sum(totals.values())
    breakdown = {
        cat: (amt, round((amt / total_expenses * 100), 2))
        for cat, amt in totals.items()
    }
    return breakdown

def plot_breakdown(breakdown):
    """
    Tworzy wykres słupkowy przedstawiający wydatki wg kategorii.

    breakdown: Słownik {kategoria: (kwota, procent)}
    """
    categories = list(breakdown.keys())
    values = [v[0] for v in breakdown.values()]
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values)
    plt.title("Wydatki wg kategorii")
    plt.xlabel("Kategoria")
    plt.ylabel("Kwota")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
