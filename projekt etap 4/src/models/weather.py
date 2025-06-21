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


    def calculate_comfort_index(self) -> int:
        """
        Oblicza komfort wędrówki (0–100) na podstawie:
         - temperatury (idealna 20–25°C)
         - opadów (każdy mm obniża wynik)
         - zachmurzenia (każdy % chmur obniża wynik)
        Wagi: temperatura 50%, opady 30%, zachmurzenie 20%.
        """
        temp = self._avg_temp
        precip = self._precipitation
        cloud = self._cloud_cover

        # 1) Skala temperatury: w idealnym punkcie (22.5°C) dajemy 100,
        #    a poza zakresem [0,40] natychmiast 0.
        if temp <= 0 or temp >= 40:
            temp_score = 0
        else:
            temp_score = 100 - abs(temp - 22.5) * (100 / 22.5)  # spadek liniowy

        # 2) Skala opadów: 0 mm → 100 pkt, każdy mm → -20 pkt, minimalnie 0
        precip_score = max(0, 100 - precip * 20)

        # 3) Skala zachmurzenia: 0% → 100 pkt, 100% → 0 pkt
        cloud_score = max(0, 100 - cloud)

        # 4) Wagi
        comfort = (
            temp_score * 0.5 +
            precip_score * 0.3 +
            cloud_score * 0.2
        )
        return int(max(0, min(100, comfort)))
