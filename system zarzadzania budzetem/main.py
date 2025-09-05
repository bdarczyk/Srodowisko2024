"""
Moduł uruchamiający aplikację Systemu Zarządzania Budżetem Osobistym.

Obsługuje:
- Wczytanie konfiguracji z pliku JSON (domyślnie config.json lub wskazany przez --config)
- Inicjalizację loggera aplikacji
- Utworzenie instancji systemu przechowywania danych (plik/baza)
- Uruchomienie głównego menu konsolowego
"""
from utils.config import load_config
from models.transaction_manager import TransactionManager
from ui.console_menu import show_menu
from utils.logger import setup_logger
import argparse
from storage.factory import StorageFactory

def main():
    """
    Główna funkcja startowa programu.

    - Parsuje argumenty z wiersza poleceń (--config)
    - Ładuje ustawienia z pliku konfiguracyjnego
    - Ustawia logger aplikacji
    - Tworzy obiekt `Storage` w zależności od konfiguracji (DB lub plik)
    - Tworzy `TransactionManager`, który zarządza transakcjami
    - Uruchamia menu konsolowe (`show_menu`)
    """
    parser = argparse.ArgumentParser(description="System Zarządzania Budżetem Osobistym")
    parser.add_argument("--config", help="Ścieżka do pliku config.json", default="config.json")
    args = parser.parse_args()

    setup_logger()
    config = load_config(args.config)
    storage = StorageFactory.from_config(config) #storage może być zarówno FileStorage, jak i DBStorage.
    manager = TransactionManager(storage)
    show_menu(manager, config)

if __name__ == "__main__":
    main()
