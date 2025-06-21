import csv
import os

class MigrationTool:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def migrate_routes_from_csv(self, csv_path):
        print(f"Migracja tras z pliku: {csv_path}")
        if not os.path.exists(csv_path):
            print("Plik nie istnieje:", csv_path)
            return

        migrated = 0
        errors = 0

        with open(csv_path, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for idx, row in enumerate(reader, 1):
                required_fields = ['name', 'region', 'start_lat', 'start_lon', 'end_lat', 'end_lon']
                missing = [field for field in required_fields if not row.get(field)]
                if missing:
                    print(f"[{idx}] Brak wymaganych pól: {missing} w wierszu {row}")
                    errors += 1
                    continue

                try:
                    with self.db_manager.connect() as conn:
                        conn.execute("""
                                   INSERT INTO routes (
                                       name, region, start_lat, start_lon, end_lat, end_lon,
                                       length_km, elevation_gain, difficulty, terrain_type, tags, description
                                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """, (
                            row['name'],
                            row['region'],
                            row['start_lat'],
                            row['start_lon'],
                            row['end_lat'],
                            row['end_lon'],
                            row['length_km'],
                            row['elevation_gain'],
                            row['difficulty'],
                            row['terrain_type'],
                            row['tags'],
                            row['description']
                        ))
                    if not self.db_manager.route_exists(row["name"], row["region"]):
                        self.db_manager.insert_route(row)
                        migrated += 1
                    else:
                        print(f"[{idx}] Trasa już istnieje w bazie: {row['name']} ({row['region']})")
                except Exception as e:
                    print(f"[{idx}] Błąd migracji trasy: {e} Wiersz: {row}")
                    errors += 1

        print(f"Migracja tras zakończona. Dodano: {migrated}, błędów: {errors}")

    # Przykład dla pogody - analogicznie
    def migrate_weather_from_csv(self, csv_path):
        print(f"Migracja pogody z pliku: {csv_path}")
        if not os.path.exists(csv_path):
            print("Plik nie istnieje:", csv_path)
            return

        migrated = 0
        errors = 0

        with open(csv_path, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for idx, row in enumerate(reader, 1):
                try:
                    with self.db_manager.connect() as conn:
                        conn.execute("""
                            INSERT OR IGNORE INTO weather_data (
                                date, location_id, avg_temp, min_temp, max_temp,
                                precipitation, sunshine_hours, cloud_cover
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row['date'],
                            row['location_id'],
                            float(row['avg_temp']) if row.get('avg_temp') else None,
                            float(row['min_temp']) if row.get('min_temp') else None,
                            float(row['max_temp']) if row.get('max_temp') else None,
                            float(row['precipitation']) if row.get('precipitation') else None,
                            float(row['sunshine_hours']) if row.get('sunshine_hours') else None,
                            float(row['cloud_cover']) if row.get('cloud_cover') else None,
                        ))
                        migrated += 1
                except Exception as e:
                    print(f"[{idx}] Błąd migracji pogody: {e} Wiersz: {row}")
                    errors += 1
        print(f"Migracja pogody zakończona. Dodano: {migrated}, błędów: {errors}")
