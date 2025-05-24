class WeatherData:
    def __init__(self, date, location_id, avg_temp, min_temp, max_temp, precipitation, sunshine_hours, cloud_cover):
        self._date = date
        self._location_id = location_id
        self._avg_temp = float(avg_temp)
        self._min_temp = float(min_temp)
        self._max_temp = float(max_temp)
        self._precipitation = float(precipitation)
        self._sunshine_hours = float(sunshine_hours) if sunshine_hours != '' else 0.0
        self._cloud_cover = float(cloud_cover)

    @property
    def date(self):
        return self._date

    @property
    def location_id(self):
        return self._location_id

    @property
    def avg_temp(self):
        return self._avg_temp

    @property
    def precipitation(self):
        return self._precipitation

    @property
    def sunshine_hours(self):
        return self._sunshine_hours

    @property
    def cloud_cover(self):
        return self._cloud_cover

    @property
    def temperature_range(self):
        return self._max_temp - self._min_temp

    # --- Metody ---
    @property
    def comfort_index(self):
        temp_score = max(0, 100 - abs(self.avg_temp - 20) * 3) # 20°C to temperatura idealna.
        precip_score = max(0, 100 - self.precipitation * 20) # Każdy 1 mm opadu zmniejsza komfort o 20 punktów
        cloud_score = max(0, 100 - self.cloud_cover * 5) # Każde 1% zachmurzenia zabiera 5 punktów
        return round(0.5 * temp_score + 0.3 * precip_score + 0.2 * cloud_score, 2) # 50% temperatura, 30%opady, 20% zachmurzenie
