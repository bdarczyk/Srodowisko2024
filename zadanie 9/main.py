from src.database_manager import DatabaseManager
from src.ui import menu

def main():
    db = DatabaseManager()
    db.initialize_database()
    menu()

if __name__ == "__main__":
    main()
