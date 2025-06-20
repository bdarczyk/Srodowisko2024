from abc import ABC, abstractmethod

class BaseStorage(ABC):
    """
    Abstrakcyjna klasa bazowa definiująca interfejs dla systemów przechowywania danych.

    Klasy dziedziczące muszą zaimplementować metody: load, save, export_to_csv.
    """
    @abstractmethod
    def load(self):
        """
        Wczytuje dane z wybranego źródła (np. pliku, bazy danych).
        return Lista obiektów Transaction
        """
        pass

    @abstractmethod
    def save(self, transactions):
        """
        Zapisuje listę transakcji do wybranego źródła danych.

        param transactions Lista obiektów Transaction
        """
        pass

    @abstractmethod
    def export_to_csv(self, transactions, filename):
        """
        Eksportuje dane do pliku CSV.

        param transactions Lista obiektów Transaction
        param filename Nazwa pliku CSV, do którego eksportujemy
        """
        pass
