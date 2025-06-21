from src.models.user_preference import UserPreference
from src.models.route import Route

class RouteRecommender:
    def __init__(self, user_preferences: UserPreference, weather_data: dict):
        self.user_preferences = user_preferences
        # słownik kluczy "location_date" → WeatherData
        self.weather_data_map = weather_data

    def recommend_routes(self, routes: list[Route], date: str) -> list[Route]:
        scored = []
        for route in routes:
            key = f"{route.region}_{date}"
            weather = self.weather_data_map.get(key)

            # 1) filtr trasowy
            if not self.user_preferences.matches_route(route):
                continue
            # 2) filtr pogodowy, jeśli mamy dane
            if weather is not None and not self.user_preferences.matches_weather(weather):
                continue

            # 3) oblicz komfort wg nowej, wagowej metody
            comfort = weather.calculate_comfort_index() if weather else 50
            route.comfort_index = comfort

            # 4) szacowany czas i kategoria
            route.estimated_time = route.estimate_time()
            route.category = route.categorize_route()

            scored.append((route, comfort))

        # 5) sortuj malejąco po komforcie
        scored.sort(key=lambda x: x[1], reverse=True)
        return [r for r, _ in scored]


