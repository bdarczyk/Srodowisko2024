import os
from src.extractors.html_route_extractor import HTMLRouteExtractor

class WebDataCollector:
    """
    Prosty kolektor HTML: czyta lokalne pliki i od razu parsuje je przez HTMLRouteExtractor.

    Metody:
      - fetch(filename: str) -> str: wczytuje zawartość pliku HTML
      - collect(filenames: list[str]) -> dict[str, dict]: czyta i parsuje wiele plików HTML,
        zwracając słownik mapujący nazwę pliku na wynik ekstrakcji HTMLRouteExtractor
    """
    def __init__(self, cache_dir: str = "data/html_cache"):
        """
        Inicjalizuje ścieżkę do katalogu z plikami HTML.
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch(self, filename: str) -> str:
        """
        Wczytuje lokalny plik HTML i zwraca jego treść jako string.
        filename może być pełną ścieżką lub nazwą pliku w cache_dir.
        """
        path = filename if os.path.isabs(filename) else os.path.join(self.cache_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Plik HTML nie istnieje: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def collect(self, filenames: list[str]) -> dict[str, dict]:
        """
        Dla każdego pliku HTML z listy:
          1. Wczytuje zawartość pliku (fetch)
          2. Parsuje HTML za pomocą HTMLRouteExtractor
          3. Zapisuje wynik extract_all() w słowniku

        Zwraca: { filename: extractor_data_dict }
        """
        results = {}
        for fn in filenames:
            try:
                html = self.fetch(fn)
                extractor = HTMLRouteExtractor()
                extractor.feed(html)
                extractor.close()
                results[fn] = extractor.extract_all()
            except Exception as e:
                print(f"Błąd przetwarzania {fn}: {e}")
        return results


if __name__ == "__main__":
    # Przykład użycia WebDataCollector z plikiem test_route.html w katalogu data/html_cache
    collector = WebDataCollector(cache_dir="../../tests/")
    # Zakładamy, że test_route.html jest już w data/html_cache/
    test_file = "test2.html"
    parsed_map = collector.collect([test_file])
    # Wyświetl wyniki
    for fn, data in parsed_map.items():
        print(f"\n-- Wyniki dla pliku: {fn}")
        print("Parametry:", data.get('params'))
        print("Opis:", data.get('description'))
        print("Obrazy:", data.get('images'))
        print("Mapy:", data.get('map_embeds'))
        print("Recenzje:", data.get('reviews'))
