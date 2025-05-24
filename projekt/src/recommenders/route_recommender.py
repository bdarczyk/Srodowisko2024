from src.models.user_preference import UserPreference
from src.models.route import Route


class RouteRecommender:
    def __init__(self, user_preferences: UserPreference, weather_data: dict):
        self.user_preferences = user_preferences
        self.weather_data_map = weather_data

    def recommend_routes(self, routes: list[Route], date: str, top_n=100) -> list[Route]:
        scored_routes = []

        for route in routes:
            location = route.region
            weather = self.weather_data_map.get(f"{location}_{date}")
            if weather and not self.user_preferences.matches_weather(weather):
                continue
            if not self.user_preferences.matches_route(route):
                continue

            comfort = weather.comfort_index if weather else 50
            route.comfort_index = comfort
            score = comfort
            scored_routes.append((route, score))

        scored_routes.sort(key=lambda x: x[1], reverse=True)
        return [r for r, _ in scored_routes[:top_n]]

