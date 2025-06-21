import re
from typing import List, Tuple

class TextProcessor:
    """
    Analiza opisów tras:
      – czasy przejścia (godziny i minuty),
      – punkty wysokościowe (metry n.p.m.),
      – współrzędne GPS (DMS),
      – ostrzeżenia (uwaga, ostrzeżenie, niebezpieczeństwo),
      – punkty charakterystyczne (szczyt, schronisko, przełęcz).
      – standaryzacja DMS → stopnie dziesiętne.
    """

    HOURS_PATTERN = re.compile(
        r'(\d+(?:\.\d+)?)\s*(?:h|godz|hours?)',
        re.IGNORECASE
    )
    MINUTES_PATTERN = re.compile(
        r'(\d+)\s*(?:min|minut)',
        re.IGNORECASE
    )
    ELEVATION_PATTERN = re.compile(
        r'(\d{3,4})\s*m\s*n\.p\.m\.',
        re.IGNORECASE
    )
    GPS_PATTERN = re.compile(
        r'([NS]?\d{1,2}[°º]\d{1,2}[\'′]\d{1,2}(?:["″]+))\s*,?\s*'
        r'([EW]?\d{1,3}[°º]\d{1,2}[\'′]\d{1,2}(?:["″]+))',
        re.IGNORECASE
    )
    ALERTS_PATTERN = re.compile(
        r'\b(uwaga|ostrzeżenie|niebezpieczeństwo|zwróć uwagę)\b.*?(?:\.|$)',
        re.IGNORECASE
    )
    POI_PATTERN = re.compile(
        r'\b(schronisko|szczyt|przełęcz)\s+'
        r'([A-ZĄĆĘŁŃÓŚŹŻ][A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż\s-]+?)(?=(?:,| oraz| i|\.))',
        re.IGNORECASE
    )

    def extract_duration(self, text: str) -> int:
        """
        Zwraca łączny czas przejścia w minutach.
        Obsługuje formaty: "2h 30min", "150 minut", "2.5 godziny".
        """
        total = 0
        h_match = self.HOURS_PATTERN.search(text)
        if h_match and h_match.group(1):
            total += int(float(h_match.group(1)) * 60)

        m_match = self.MINUTES_PATTERN.search(text)
        if m_match and m_match.group(1):
            total += int(m_match.group(1))

        return total

    def extract_elevation_points(self, text: str) -> List[int]:
        """
        Zwraca listę wartości wysokości (metry n.p.m.) znalezionych w tekście.
        """
        return [int(m) for (m) in self.ELEVATION_PATTERN.findall(text)]

    def extract_gps_coords(self, text: str) -> List[Tuple[str, str]]:
        """
        Zwraca listę krotek DMS: [(lat_str, lon_str), ...].
        """
        return self.GPS_PATTERN.findall(text)

    def extract_alerts(self, text: str) -> List[str]:
        """
        Zwraca listę pełnych fragmentów zdań rozpoczynających się od słów ostrzegawczych.
        """
        return [m.group(0).strip() for m in self.ALERTS_PATTERN.finditer(text)]

    def extract_points_of_interest(self, text: str) -> List[Tuple[str, str]]:
        """
        Zwraca listę punktów charakterystycznych jako (typ, nazwa),
        np. ('szczyt', 'Rysy').
        """
        return [
            (m.group(1).lower(), m.group(2).strip())
            for m in self.POI_PATTERN.finditer(text)
        ]

    def standardize_gps(self, coords: List[Tuple[str, str]]) -> List[Tuple[float, float]]:
        """
        Konwertuje DMS na stopnie dziesiętne:
        N/S wskazuje znak dodatni/ujemny dla szerokości,
        E/W – dla długości.
        """
        def dms_to_dd(dms: str) -> float:
            parts = re.findall(r'(\d+)', dms)
            deg, mn, sec = map(float, parts[:3])
            dd = deg + mn / 60 + sec / 3600
            if dms[0].upper() in ('S', 'W'):
                dd = -dd
            return dd

        return [(dms_to_dd(lat), dms_to_dd(lon)) for lat, lon in coords]
