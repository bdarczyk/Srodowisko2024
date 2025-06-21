class Route:
    DIFFICULTY_NAMES = {1: 'łatwa', 2: 'średnia', 3: 'trudna', 4: 'ekstremalna', 5: 'zawodowa'}
    DIFFICULTY_MULTIPLIERS = {1: 1.0, 2: 1.2, 3: 1.4, 4: 1.6, 5: 1.8}

    TERRAIN_MULTIPLIERS = {
        'asfalt': 1.0,
        'szlak górski': 0.7,
        'leśny': 0.8,
        'piaszczysty': 0.6,
    }

    def __init__(self, id, name, region, start_lat, start_lon, end_lat, end_lon,
                 length_km, elevation_gain, difficulty, terrain_type, tags, description, reviews):
        self._id = id
        self._name = name
        self._region = region
        self._start_lat = float(start_lat)
        self._start_lon = float(start_lon)
        self._end_lat = float(end_lat)
        self._end_lon = float(end_lon)
        self._length_km = float(length_km)
        self._elevation_gain = float(elevation_gain)
        self._difficulty = int(difficulty)
        self._terrain_type = terrain_type.lower()
        self._tags = tags.split(",") if isinstance(tags, str) else tags
        self._description = description
        self._reviews = reviews if reviews is not None else []

        self.comfort_index = None
        self.estimated_time = None
        self.category = None

    # Właściwości
    @property
    def name(self): return self._name

    @property
    def id(self):
        return self._id

    @property
    def region(self): return self._region

    @property
    def length_km(self): return self._length_km

    @property
    def elevation_gain(self): return self._elevation_gain

    @property
    def difficulty(self): return self._difficulty

    @property
    def terrain_type(self): return self._terrain_type

    @property
    def tags(self): return self._tags

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def reviews(self) -> list[str]:
        """Zwraca listę recenzji przypisanych do trasy."""
        return self._reviews

    @reviews.setter
    def reviews(self, value: list[str]):
        if not isinstance(value, list):
            raise ValueError("reviews musi być listą tekstów")
        self._reviews = value


    def estimate_time(self):
        base_speed = 4.0 # domyslna predkosc
        terrain_factor = self.TERRAIN_MULTIPLIERS.get(self._terrain_type, 0.8) # domyslnie 0.8
        difficulty_factor = self.DIFFICULTY_MULTIPLIERS.get(self._difficulty, 1.2) # domyslnie 1.2

        time_hours = self._length_km / (base_speed * terrain_factor)
        time_hours += self._elevation_gain / 600.0
        time_hours *= difficulty_factor

        minutes = round(time_hours * 60)
        self.estimated_time = minutes
        return minutes

    def matches_preferences(self, preferences):
        if self._length_km > preferences.max_length:
            return False
        if self._difficulty > preferences.max_difficulty:
            return False
        if preferences.preferred_terrain and self._terrain_type not in preferences.preferred_terrain:
            return False
        return True

    def categorize_route(self):
        if self._length_km < 5 and self._elevation_gain < 100:
            self.category = "rodzinna"
        elif "view" in self._tags:
            self.category = "widokowa"
        elif self._elevation_gain > 600 or self._length_km > 15:
            self.category = "sportowa"
        elif self._difficulty >= 3:
            self.category = "ekstremalna"
        else:
            self.category = "ogólna"
        return self.category

