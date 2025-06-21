import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Nawiązuje połączenie z bazą SQLite."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row # pozwala odczytywać dane jako dict
        self.conn.execute('PRAGMA foreign_keys = ON;')
        return self.conn

    def initialize_database(self, schema_path):
        """Tworzy tabele w bazie na podstawie pliku SQL."""
        if not self.conn:
            self.connect()
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        self.conn.executescript(schema)
        self.conn.commit()

    def close(self):
        """Zamyka połączenie z bazą."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, sql, params=()):
        """Wykonuje dowolne zapytanie SQL (INSERT, UPDATE, DELETE, ...)."""
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql, params=()):
        """Zwraca wyniki zapytania SELECT."""
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    # --- Walidacja spójności danych ---
    def count_records(self, table):
        """Zwraca liczbę rekordów w wybranej tabeli."""
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        return cur.fetchone()[0]

    def validate_integrity(self):
        """Sprawdza podstawową integralność bazy."""
        try:
            # Przykładowo: czy są jakiekolwiek trasy i dane pogodowe
            routes = self.count_records("routes")
            weather = self.count_records("weather_data")
            return {
                "routes": routes,
                "weather_data": weather,
                "ok": routes > 0 and weather > 0
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def route_exists(self, name, region):
        with self.connect() as conn:
            cur = conn.execute(
                "SELECT 1 FROM routes WHERE name=? AND region=? LIMIT 1", (name, region)
            )
            return cur.fetchone() is not None

    def insert_route(self, route_data):
        with self.connect() as conn:
            conn.execute("""
                INSERT INTO routes (
                    name, region, start_lat, start_lon, end_lat, end_lon, length_km,
                    elevation_gain, difficulty, terrain_type, tags, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                route_data["name"],
                route_data["region"],
                route_data["start_lat"],
                route_data["start_lon"],
                route_data["end_lat"],
                route_data["end_lon"],
                route_data["length_km"],
                route_data["elevation_gain"],
                route_data["difficulty"],
                route_data["terrain_type"],
                route_data["tags"],
                route_data["description"]
            ))