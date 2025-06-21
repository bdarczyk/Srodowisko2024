from src.database.databse_manager import DatabaseManager
from src.database.migration_tool import MigrationTool
from src.database.repositories.route_repository import RouteRepository
from src.database.repositories.weather_repository import WeatherRepository
from src.database.repositories.user_repository import UserPreferenceRepository
from src.data_handlers.route_data_manager import RouteDataManager, DatabaseReports
from src.data_handlers.weather_data_manager import WeatherDataManager, DatabaseAdmin
from src.ui.user_interface import UserInterface

import os

def main():
    db_path = 'data/database/routes.db'
    schema_path = 'sql/schema.sql'
    backup_dir = 'data/backups/'
    os.makedirs(backup_dir, exist_ok=True)

    # Inicjalizacja komponentów
    db_manager = DatabaseManager(db_path)
    db_manager.initialize_database(schema_path)
    migration_tool = MigrationTool(db_manager)
    route_repo = RouteRepository(db_manager)
    weather_repo = WeatherRepository(db_manager)
    user_repo = UserPreferenceRepository(db_manager)
    route_manager = RouteDataManager(route_repo)
    weather_manager = WeatherDataManager(weather_repo)
    admin = DatabaseAdmin(db_manager, db_path, backup_dir)
    reports = DatabaseReports(db_manager, route_repo, weather_repo)
    ui = UserInterface()

    while True:
        ui.main_menu()
        choice = ui.get_user_choice().strip()
        if choice == "1":
            user_prefs = ui.get_user_preferences()
            user_repo.save_preferences(user_prefs)
            routes = route_manager.filter_routes(
                region=user_prefs["location_id"],
                max_difficulty=user_prefs["max_difficulty"],
                max_length=user_prefs["max_length_km"]
            )
            weather_data = {}  # Tu możesz pobrać pogodę, jeśli chcesz.
            ui.display_recommendations(routes, weather_data, user_prefs["date"])

        elif choice == "2":
            print("\nDodawanie nowej trasy:")
            name = input("Nazwa trasy: ")
            region = input("Region: ")
            start_lat = float(input("Start - szerokość geograficzna: "))
            start_lon = float(input("Start - długość geograficzna: "))
            end_lat = float(input("Koniec - szerokość geograficzna: "))
            end_lon = float(input("Koniec - długość geograficzna: "))
            length_km = float(input("Długość trasy (km): "))
            elevation_gain = int(input("Przewyższenie (m): "))
            difficulty = int(input("Trudność (1-5): "))
            terrain_type = input("Typ terenu: ")
            tags = input("Tagi (oddzielone przecinkami): ")
            description = input("Opis trasy: ")
            route_data = {
                'name': name,
                'region': region,
                'start_lat': start_lat,
                'start_lon': start_lon,
                'end_lat': end_lat,
                'end_lon': end_lon,
                'length_km': length_km,
                'elevation_gain': elevation_gain,
                'difficulty': difficulty,
                'terrain_type': terrain_type,
                'tags': tags,
                'description': description
            }
            try:
                route_repo.add_route(route_data)
                ui.show_message("Dodano nową trasę!")
            except Exception as e:
                ui.show_message(f"Błąd podczas dodawania trasy: {e}")

        elif choice == "3":
            admin.show_database_stats()
            reports.most_popular_regions()
            reports.difficulty_summary()
            reports.routes_without_weather()
            reports.weather_stats_for_regions()

        elif choice == "4":
            admin.create_backup()

        elif choice == "5":
            migration_tool.migrate_routes_from_csv('data/legacy/trasy.csv')
            migration_tool.migrate_weather_from_csv('data/legacy/pogoda.csv')

        elif choice == "6":
            print("\nZ której tabeli chcesz wyświetlić rekordy?")
            print("1 - routes")
            print("2 - weather_data")
            print("3 - user_preference")
            table_choice = input("Wybierz numer tabeli: ").strip()
            table_map = {
                "1": "routes",
                "2": "weather_data",
                "3": "user_preferences"
            }
            table = table_map.get(table_choice)
            if not table:
                ui.show_message("Nieprawidłowy wybór tabeli.")
                continue
            try:
                records = db_manager.query(f"SELECT * FROM {table};")
                if not records:
                    ui.show_message("Brak rekordów w tej tabeli.")
                else:
                    print(f"\nRekordy z tabeli {table}:")
                    for row in records:
                        print(dict(row))
            except Exception as e:
                ui.show_message(f"Błąd podczas pobierania rekordów: {e}")

        elif choice == "7":
            admin.list_backups()
            backup_name = input("Podaj nazwę kopii do przywrócenia: ")
            admin.restore_backup(backup_name)
            break

        elif choice == "8":
            table = input("Podaj nazwę tabeli: ")
            date_field = input("Podaj nazwę pola z datą (np. 'date'): ")
            max_age_days = int(input("Rekordy starsze niż ile dni usunąć?: "))
            admin.clean_old_data(table, date_field, max_age_days)
            break


        elif choice == "9":
            location = input("Podaj lokalizacje: ")
            date = input("Podaj datę (YYYY-MM-DD): ")
            try:
                result = weather_manager.get_weather_for(location, date)
                if result:
                    print(f"Pogoda dla lokalizacji ({result['location_id']}) na dzień {result['date']}:")
                    print(f"Średnia temperatura: {result['avg_temp']}°C")
                    print(f"Min: {result['min_temp']}°C, Max: {result['max_temp']}°C")
                    print(f"Opady: {result['precipitation']} mm")
                    print(f"Zachmurzenie: {result['cloud_cover']}%")
                else:
                    print("Brak danych pogodowych dla tej lokalizacji i daty.")
            except Exception as e:
                print(f"Błąd podczas pobierania pogody: {e}")
            break

        elif choice == "0":
            print("Do zobaczenia!")
            break
        else:
            ui.show_message("Nieznana opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
