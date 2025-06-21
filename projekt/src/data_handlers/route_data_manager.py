from src.models.route import Route
import csv
class RouteDataManager:
    def __init__(self, routes_file: str, reviews_file: str = None):
        """
        routes_file:   ścieżka do CSV z trasami
        reviews_file:  (opcjonalnie) ścieżka do CSV z recenzjami w formacie
                       route_id;review_text
        """
        self.routes_file = routes_file
        self.reviews_file = reviews_file
        self._routes = []

    def load_routes(self) -> list[Route]:
        # 1) Wczytaj recenzje do zwykłego słownika
        reviews_map = {}
        if self.reviews_file:
            with open(self.reviews_file, encoding='utf-8-sig', newline='') as rf:
                rev_reader = csv.DictReader(rf, delimiter=';')
                for rev_row in rev_reader:
                    rid = int(rev_row['route_id'])
                    if rid not in reviews_map:
                        reviews_map[rid] = []
                    reviews_map[rid].append(rev_row['review_text'])

        # 2) Wczytaj trasy
        with open(self.routes_file, encoding='utf-8-sig', newline='') as cf:
            reader = csv.DictReader(cf, delimiter=';')
            for row in reader:
                rid = int(row['id'])
                route = Route(
                    id=rid,
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
                    tags=row['tags'].split(','),
                    description=row.get('description', ""),
                    reviews=reviews_map.get(rid, [])
                )
                self._routes.append(route)
        return self._routes

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, new_routes):
        if isinstance(new_routes, list) and all(isinstance(r, Route) for r in new_routes):
            self._routes = new_routes
        else:
            raise ValueError("routes musi zawierać listę tras instancji Route")