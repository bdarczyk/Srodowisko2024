class UserPreferenceRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def save_preferences(self, preferences):
        with self.db_manager.connect() as conn:
            conn.execute("""
                INSERT INTO user_preferences (
                    user_name, preferred_temp_min, preferred_temp_max, max_precipitation,
                    max_difficulty, max_length_km, preferred_terrain_types
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                preferences.get('user_name', 'default'),
                preferences.get('preferred_temp_min'),
                preferences.get('preferred_temp_max'),
                preferences.get('max_precipitation'),
                preferences.get('max_difficulty'),
                preferences.get('max_length_km'),
                preferences.get('preferred_terrain_types')
            ))
            conn.commit()

    def get_preferences(self, user_name='default'):
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_preferences WHERE user_name=?
                ORDER BY updated_at DESC LIMIT 1
            """, (user_name,))
            return cursor.fetchone()
