from src.models.user_preference import UserPreference

class UserInterface:
    def get_user_preferences(self):
        print("Podaj swoje preferencje turystyczne:")
        min_temp = float(input("Minimalna temperatura (°C): "))
        max_temp = float(input("Maksymalna temperatura (°C): "))
        precipitation = float(input("Maksymalna tolerancja opadów (mm): "))
        max_difficulty = int(input("Maksymalna trudność trasy (1–5): "))
        max_length = float(input("Maksymalna długość trasy (km): "))
        date = input("Podaj datę wycieczki (YYYY-MM-DD): ")
        location = input("Podaj lokalizację (np. Gdańsk): ")

        return UserPreference(
            preferred_temp_range=(min_temp, max_temp),
            precipitation_tolerance=precipitation,
            max_difficulty=max_difficulty,
            max_route_length=max_length,
            date=date,
            location_id=location
        )

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