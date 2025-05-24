from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.recommenders.route_recommender import RouteRecommender
from src.ui.user_interface import UserInterface

def main():
    # Wczytaj dane
    route_manager = RouteDataManager('data/trasy.csv')
    weather_manager = WeatherDataManager('data/pogoda.csv')
    routes = route_manager.load_routes()

    # Pobierz preferencje od użytkownika
    ui = UserInterface()
    preferences = ui.get_user_preferences()

    date = preferences._date
    weather_by_region = { # Tworzy słownik: {region_data: dane pogodowe} tylko dla tej konkretnej daty
        f"{route.region}_{date}": weather_manager.get_weather_for(route.region, date)
        for route in routes
    }


    # Rekomendacje
    recommender = RouteRecommender(preferences, weather_by_region)
    recommendations = recommender.recommend_routes(routes, date)

    # Wyświetl wyniki
    ui.display_recommendations(recommendations, weather_by_region, date)

if __name__ == "__main__":
    main()