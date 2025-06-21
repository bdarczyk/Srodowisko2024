class RouteRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_route(self, route_data):
        self.db_manager.insert_route(route_data)

    def update_route(self, route_id, updates):
        """Aktualizuje wskazane pola w trasie"""
        keys = []
        values = []
        for k, v in updates.items():
            keys.append(f"{k}=?")
            values.append(v)
        values.append(route_id)
        with self.db_manager.connect() as conn:
            conn.execute(
                f"UPDATE routes SET {', '.join(keys)} WHERE id=?",
                values
            )
            conn.commit()

    def filter_routes(self, region=None, min_length=None, max_length=None, min_difficulty=None, max_difficulty=None):
        """Dynamiczne filtrowanie tras po różnych parametrach"""
        query = "SELECT * FROM routes WHERE 1=1"
        params = []
        if region:
            query += " AND region=?"
            params.append(region)
        if min_length:
            query += " AND length_km>=?"
            params.append(min_length)
        if max_length:
            query += " AND length_km<=?"
            params.append(max_length)
        if min_difficulty:
            query += " AND difficulty>=?"
            params.append(min_difficulty)
        if max_difficulty:
            query += " AND difficulty<=?"
            params.append(max_difficulty)
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

