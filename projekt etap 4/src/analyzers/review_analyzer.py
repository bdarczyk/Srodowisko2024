import re
from typing import List

class ReviewAnalyzer:
    """
    Analiza recenzji tras:
      – ekstrakcja oceny (gwiazdki, skala 0-5 i 0-10),
      – analiza sentymentu (pozytywny, negatywny, neutralny),
      – wydobywanie aspektów (np. widoki, trudność, oznakowanie),
      – ekstrakcja dat jako tekst.
    """

    RATING_PATTERN = re.compile(
        r'(★{1,5})|(\d(?:\.\d)?)/5|(\d{1,2})/10',
        re.IGNORECASE
    )
    DATE_PATTERN = re.compile(r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b')
    ASPECTS = ['widok', 'trudność', 'oznaczenie', 'szlak', 'długość']

    def extract_rating(self, text: str) -> float:
        """
        Zwraca ocenę w skali 0–5:
          ★★★★      → 4.0
          3.5/5     → 3.5
          8/10      → 4.0
        """
        m = self.RATING_PATTERN.search(text)
        if not m:
            return 0.0
        stars, five, ten = m.groups()
        if stars:
            return float(len(stars))
        if five:
            return float(five)
        if ten:
            return float(ten) / 2
        return 0.0

    def analyze_sentiment(self, text: str) -> str:
        """
        Prosty wzorzec sentymentu:
          jeśli występują słowa pozytywne → 'positive',
          jeśli występują słowa negatywne → 'negative',
          inaczej → 'neutral'.
        """
        positive = re.search(r'\b(świetna|super|polecam|wspaniały|piękne|warty)\b', text, re.IGNORECASE)
        negative = re.search(r'\b(źle|nie polecam|ostrzegam|uwaga|trudny|brak|słabe)\b', text, re.IGNORECASE)
        if positive and not negative:
            return 'pozytywny'
        if negative and not positive:
            return 'negatywny'
        return 'neutralny'

    def extract_aspects(self, text: str) -> List[str]:
        """
        Zwraca listę predefiniowanych aspektów występujących w tekście.
        """
        found = []
        for aspect in self.ASPECTS:
            if re.search(rf'\b{aspect}\w*\b', text, re.IGNORECASE):
                found.append(aspect)
        return found

    def extract_dates(self, text: str) -> List[str]:
        """
        Wyciąga daty w formatach: dd.mm.yyyy, dd/mm/yy itp.
        i zwraca listę dopasowanych łańcuchów (stringów).
        """
        return [m.group(0) for m in self.DATE_PATTERN.finditer(text)]


# --- Test wewnętrzny ---
"""
if __name__ == "__main__":
    import csv

    ra = ReviewAnalyzer()
    path = "../../data/routes/reviews.csv"  # dostosuj ścieżkę do pliku z recenzjami

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            text = row["review_text"]
            print(f"--- Recenzja: {text}")
            print("Ocena:      ", ra.extract_rating(text))
            print("Sentyment:  ", ra.analyze_sentiment(text))
            print("Aspekty:    ", ra.extract_aspects(text))
            print("Daty:       ", ra.extract_dates(text))
            print()
"""