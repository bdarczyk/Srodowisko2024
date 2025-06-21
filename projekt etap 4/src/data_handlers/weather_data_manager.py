from src.database.repositories.weather_repository import WeatherRepository
import os, shutil
from datetime import datetime

class WeatherDataManager:
    def __init__(self, weather_repository: WeatherRepository):
        self.weather_repository = weather_repository

    def get_weather_for(self, location_id, date):
        row = self.weather_repository.get_weather_for_location_and_date(location_id, date)
        if not row:
            print("Brak danych pogodowych dla tej lokalizacji i daty.")
            return None
        # row to tuple w kolejności jak w bazie:
        # (id, date, location_id, avg_temp, min_temp, max_temp, precipitation, sunshine_hours, cloud_cover)
        return {
            "date": row[1],
            "location_id": row[2],
            "avg_temp": row[3],
            "min_temp": row[4],
            "max_temp": row[5],
            "precipitation": row[6],
            "sunshine_hours": row[7],
            "cloud_cover": row[8]
        }

class DatabaseAdmin:
    def __init__(self, db_manager, db_path, backup_dir='data/backups/'):
        self.db_manager = db_manager
        self.db_path = db_path
        self.backup_dir = backup_dir

    def show_database_stats(self):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM routes")
            routes_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            weather_count = cursor.fetchone()[0]
        print(f"Liczba tras w bazie: {routes_count}")
        print(f"Liczba rekordów pogodowych: {weather_count}")

    def create_backup(self):
        backup_name = f"routes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(self.backup_dir, backup_name)
        shutil.copy2(self.db_path, backup_path)
        print(f"Kopia zapasowa utworzona: {backup_path}")

    def list_backups(self):
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.db')]
        if not backups:
            print("Brak kopii zapasowych.")
        else:
            print("Dostępne kopie zapasowe:")
            for f in backups:
                print("  -", f)

    def restore_backup(self, backup_name):
        backup_path = os.path.join(self.backup_dir, backup_name)
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, self.db_path)
            print(f"Przywrócono bazę z kopii: {backup_name}")
        else:
            print("Wybrana kopia nie istnieje.")

    def clean_old_data(self, table, date_field, max_age_days):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {table} WHERE {date_field} < date('now', '-{max_age_days} day')"
            )
            deleted = cursor.rowcount
            conn.commit()
        print(f"Usunięto {deleted} rekordów z tabeli {table} starszych niż {max_age_days} dni.")
