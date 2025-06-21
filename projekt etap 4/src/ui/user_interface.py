class UserInterface:
    def main_menu(self):
        print("=== REKOMENDATOR TRAS TURYSTYCZNYCH ===")
        print("1. Znajdź rekomendowane trasy")
        print("2. Dodaj nową trasę")
        print("3. Statystyki bazy danych")
        print("4. Utwórz kopię zapasową")
        print("5. Importuj dane z CSV")
        print("6. Wyświetl rekordy z bazy")
        print("7. Przywróć bazę z kopii zapasowej")
        print("8. Wyczyść stare dane z tabeli")
        print("9. Wyświetl dane pogodowe dla daty i lokalizacji")
        print("0. Wyjście")

    def get_user_choice(self):
        return input("Wybierz opcję: ")

    def get_user_preferences(self):
        print("Podaj swoje preferencje turystyczne:")
        min_temp = float(input("Minimalna temperatura (°C): "))
        max_temp = float(input("Maksymalna temperatura (°C): "))
        precipitation = float(input("Maksymalna tolerancja opadów (mm): "))
        max_difficulty = int(input("Maksymalna trudność trasy (1–5): "))
        max_length = float(input("Maksymalna długość trasy (km): "))
        date = input("Podaj datę wycieczki (YYYY-MM-DD): ")
        location_id = input("Podaj lokalizację (np. Gdańsk): ")

        return {
            "preferred_temp_min": min_temp,
            "preferred_temp_max": max_temp,
            "max_precipitation": precipitation,
            "max_difficulty": max_difficulty,
            "max_length_km": max_length,
            "date": date,
            "location_id": location_id,
            "user_name": "default",
            "preferred_terrain_types": None
        }

    def show_message(self, msg):
        print(f"\n{msg}\n")


    def format_duration(self, minutes: float) -> str:
        total_minutes = int(round(minutes))
        hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        if hours > 0 and remaining_minutes > 0:
            return f"{hours}h {remaining_minutes}min"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{remaining_minutes}min"

    def display_recommendations(self, routes, weather_data, date: str):
        print(f"\nRekomendowane trasy na dzień {date}:\n")
        if not routes:
            print("Brak tras spełniających Twoje preferencje.")
            return

        for i, route in enumerate(routes, 1):
            duration = self.format_duration(route.estimated_time or route.estimate_time())
            key = f"{route.region}_{date}"
            weather = weather_data.get(key)
            # liczymy comfort na podstawie WeatherData
            if weather:
                comfort = weather.calculate_comfort_index()
            else:
                comfort = None
            category = route.category or route.categorize_route()
            print(f"{i}. {route.name} ({route.region})")
            print(f"   Długość: {route.length_km} km")
            print(f"   Trudność: {route.difficulty}/5")
            print(f"   Szacowany czas: {duration}")
            if comfort is not None:
                print(f"   Komfort pogodowy: {comfort}/100")
            else:
                print("   Brak danych pogodowych")
            print(f"   Kategoria trasy: {category}\n")