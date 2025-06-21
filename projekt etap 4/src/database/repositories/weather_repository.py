class WeatherRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_weather(self, weather_data):
        with self.db_manager.connect() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO weather_data (
                    date, location_lat, location_lon, avg_temp, min_temp, max_temp,
                    precipitation, sunshine_hours, cloud_cover
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                weather_data['date'],
                weather_data['location_lat'],
                weather_data['location_lon'],
                weather_data.get('avg_temp'),
                weather_data.get('min_temp'),
                weather_data.get('max_temp'),
                weather_data.get('precipitation'),
                weather_data.get('sunshine_hours'),
                weather_data.get('cloud_cover')
            ))
            conn.commit()

    def get_weather_for_location_and_date(self, location_id, date):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM weather_data
                WHERE location_id=? AND date=?
            """, (location_id, date))
            return cursor.fetchone()