from storage.file_storage import FileStorage
from storage.database_storage import DBStorage

class StorageFactory:
    """
    Fabryka tworząca instancję systemu przechowywania danych
    na podstawie ustawień konfiguracyjnych.
    """
    @classmethod
    def from_config(cls, config):
        """
        Tworzy obiekt FileStorage na podstawie konfiguracji.
        onfig Słownik konfiguracji (np. wczytany z config.json)
        return Instancja FileStorage z odpowiednią ścieżką pliku
        """
        if config.get("use_db", False):
            return DBStorage()
        return FileStorage(config.get("data_file", "data.json"))
