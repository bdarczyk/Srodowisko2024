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
                key = f"{row['location_id']}_{row['date']}"

                self.weather_data[key] = weather  # zmiana z listy na słownik
        return self.weather_data

    def get_weather_for(self, location_id, date):
        key = f"{location_id}_{date}"
        return self.weather_data.get(key)
