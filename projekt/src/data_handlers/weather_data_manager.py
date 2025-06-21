import csv
from src.models.weather import WeatherData

class WeatherDataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.weather_data = {}

    def load_weather(self):
        with open(self.file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                weather = WeatherData(
                    date=row["date"],
                    location_id=row["location_id"],
                    avg_temp=row["avg_temp"],
                    min_temp=row["min_temp"],
                    max_temp=row["max_temp"],
                    precipitation=row["precipitation"],
                    sunshine_hours=row["sunshine_hours"],
                    cloud_cover=row["cloud_cover"]
                )
                key = f"{row['location_id']}_{row['date']}" # tworzy klucz np. Gdansk_2025-05-24

                self.weather_data[key] = weather  # zmiana z listy na słownik
        return self.weather_data

    def get_weather_for(self, location_id, date): # Zwraca dane pogodowe dla klucza z load_weather
        key = f"{location_id}_{date}"
        return self.weather_data.get(key)

    def get_stats_for_location(self, location_id):
        """
        Zwraca statystyki pogodowe dla location_id:
        - avg_temp: średnia temperatura
        - sunny_days: liczba dni słonecznych
        - total_days: łączna liczba dni w danych
        """
        data = [w for w in self.weather_data.values() if w.location_id == location_id]
        if not data:
            return {
                'avg_temp': None,
                'total_days': 0
            }
        temps = [w.avg_temp for w in data]
        return {
            'avg_temp': sum(temps) / len(temps),
            'total_days': len(data)
        }

