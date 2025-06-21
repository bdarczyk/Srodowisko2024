class UserPreference:
    def __init__(self, preferred_temp_range=None, precipitation_tolerance=None,
                 max_difficulty=None, max_route_length=None, date=None, location_id=None):
        self._preferred_temp_range = preferred_temp_range
        self._precipitation_tolerance = precipitation_tolerance
        self._max_difficulty = max_difficulty
        self._max_route_length = max_route_length
        self._date = date
        self._location_id = location_id

    @property
    def date(self):
        return self._date
    # --- Właściwości z enkapsulacją ---
    @property
    def preferred_temp_range(self):
        return self._preferred_temp_range

    @preferred_temp_range.setter
    def preferred_temp_range(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            self._preferred_temp_range = value
        else:
            raise ValueError("Zakres temperatury musi być krotką (min, max)")

    @property
    def precipitation_tolerance(self):
        return self._precipitation_tolerance

    @precipitation_tolerance.setter
    def precipitation_tolerance(self, value):
        self._precipitation_tolerance = float(value)

    @property
    def max_difficulty(self):
        return self._max_difficulty

    @max_difficulty.setter
    def max_difficulty(self, value):
        self._max_difficulty = int(value)

    @property
    def max_route_length(self):
        return self._max_route_length

    @max_route_length.setter
    def max_route_length(self, value):
        self._max_route_length = float(value)

    # ZAMIANA property region → location_id
    """@property
    def location_id(self):
        return self._location_id

    @location_id.setter
    def location_id(self, value):
        self._location_id = value

    @property
    def selected_date(self):
        return self._date"""

# --- Metody logiczne ---
    def matches_route(self, route):
        #Sprawdza, czy trasa spełnia preferencje dotyczące długości i trudności
        if self.max_route_length is not None and route.length_km > self.max_route_length:
            return False
        if self.max_difficulty is not None and route.difficulty > self.max_difficulty:
            return False
        return True

    def matches_weather(self, weather_data):
        #Sprawdza, czy warunki pogodowe są zgodne z preferencjami
        if self.preferred_temp_range:
            min_temp, max_temp = self.preferred_temp_range
            if not (min_temp <= weather_data.avg_temp <= max_temp):
                return False
        if self.precipitation_tolerance is not None:
            if weather_data.precipitation > self.precipitation_tolerance:
                return False
        return True

    """def matches(self, route, weather_data):
        return self.matches_route(route) and self.matches_weather(weather_data)

    def update_preferences(self,preferred_temp_range=None,precipitation_tolerance=None,
        max_difficulty=None,max_route_length=None,date=None,location_id=None):

        if preferred_temp_range is not None:
            self.preferred_temp_range = preferred_temp_range
        if precipitation_tolerance is not None:
            self.precipitation_tolerance = precipitation_tolerance
        if max_difficulty is not None:
            self.max_difficulty = max_difficulty
        if max_route_length is not None:
            self.max_route_length = max_route_length
        if date is not None:
            self._date = date
        if location_id is not None:
            self._location_id = location_id"""