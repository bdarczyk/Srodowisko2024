import csv
from src.models.route import Route

class RouteDataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self._routes = []

    def load_routes(self):
        with open(self.file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                route = Route(
                    id=int(row['id']),
                    name=row['name'],
                    region=row['region'],
                    start_lat=float(row['start_lat']),
                    start_lon=float(row['start_lon']),
                    end_lat=float(row['end_lat']),
                    end_lon=float(row['end_lon']),
                    length_km=float(row['length_km']),
                    elevation_gain=int(row['elevation_gain']),
                    difficulty=int(row['difficulty']),
                    terrain_type=row['terrain_type'],
                    tags=row['tags'].split(',')
                )
                self._routes.append(route)
        return self.routes

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, new_routes):
        """Pozwala na nadpisanie listy tras."""
        if isinstance(new_routes, list) and all(isinstance(r, Route) for r in new_routes): # isinstance sprawdza czy dana wartosc sie zgadza
            self._routes = new_routes
        else:
            raise ValueError("routes musi zawierać listę tras będących instancjami klasy Route")

