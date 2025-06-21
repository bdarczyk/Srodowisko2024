-- Tabela tras
CREATE TABLE if not exists routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    region TEXT,
    start_lat REAL NOT NULL,
    start_lon REAL NOT NULL,
    end_lat REAL NOT NULL,
    end_lon REAL NOT NULL,
    length_km REAL,
    elevation_gain INTEGER,
    difficulty INTEGER CHECK (difficulty BETWEEN 1 AND 5),
    terrain_type TEXT,
    tags TEXT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela danych pogodowych
CREATE TABLE if not exists weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    location_id REAL NOT NULL,
    avg_temp REAL,
    min_temp REAL,
    max_temp REAL,
    precipitation REAL,
    sunshine_hours REAL,
    cloud_cover INTEGER,
    UNIQUE(date, location_id)
);

-- Tabela preferencji użytkownika
CREATE TABLE if not exists user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT DEFAULT 'default',
    preferred_temp_min REAL,
    preferred_temp_max REAL,
    max_precipitation REAL,
    max_difficulty INTEGER,
    max_length_km REAL,
    preferred_terrain_types TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indeksy dla wydajności
CREATE INDEX if not exists idx_routes_region ON routes(region);
CREATE INDEX if not exists idx_routes_difficulty ON routes(difficulty);
CREATE INDEX if not exists idx_weather_date ON weather_data(date);