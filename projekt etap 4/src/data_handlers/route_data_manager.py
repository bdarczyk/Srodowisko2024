from src.models.route import Route
from src.database.repositories.route_repository import RouteRepository
from src.database.repositories.weather_repository import WeatherRepository

class RouteDataManager:
    def __init__(self, route_repository: RouteRepository):
        self.route_repository = route_repository

    def filter_routes(self, filters):
        rows = self.route_repository.filter_routes(filters)
        routes = []
        for row in rows:
            route = Route(
                id=row[0],
                name=row[1],
                region=row[2],
                start_lat=row[3],
                start_lon=row[4],
                end_lat=row[5],
                end_lon=row[6],
                length_km=row[7],
                elevation_gain=row[8],
                difficulty=row[9],
                terrain_type=row[10],
                tags=row[11].split(",") if row[11] else [],
                description=row[12],
                reviews=[]
            )
            routes.append(route)
        return routes


class DatabaseReports:
    def __init__(self, db_manager, route_repository: RouteRepository, weather_repository: WeatherRepository):
        self.db_manager = db_manager
        self.route_repository = route_repository
        self.weather_repository = weather_repository

    def most_popular_regions(self, top_n=5):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT region, COUNT(*) as count
                FROM routes
                GROUP BY region
                ORDER BY count DESC
                LIMIT ?
            """, (top_n,))
            results = cursor.fetchall()
        print("Najpopularniejsze regiony:")
        for region, count in results:
            print(f"  {region}: {count} tras")

    def difficulty_summary(self):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT difficulty, COUNT(*) FROM routes
                GROUP BY difficulty
                ORDER BY difficulty
            """)
            results = cursor.fetchall()
        print("Podsumowanie tras według trudności:")
        for difficulty, count in results:
            print(f"  Trudność {difficulty}: {count} tras")

    def routes_without_weather(self):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id, r.name, r.region
                FROM routes r
                LEFT JOIN weather_data w
                    ON r.region = w.location_id
                WHERE w.id IS NULL
            """)
            results = cursor.fetchall()
        print("Trasy bez danych pogodowych:")
        for r in results:
            print(f"  ID {r[0]}: {r[1]} ({r[2]})")

    def weather_stats_for_regions(self):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.region, AVG(w.avg_temp), SUM(w.precipitation)
                FROM routes r
                JOIN weather_data w
                    ON r.region = w.location_id
                GROUP BY r.region
            """)
            results = cursor.fetchall()
        print("Statystyki pogodowe dla regionów:")
        for region, avg_temp, total_precip in results:
            print(f"  {region}: Śr. temp: {avg_temp:.1f}°C, Suma opadów: {total_precip:.1f}mm")
