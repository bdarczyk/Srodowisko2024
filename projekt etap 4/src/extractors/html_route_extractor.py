from html.parser import HTMLParser

class HTMLRouteExtractor(HTMLParser):
    """
    Parsuje dokument HTML tras:
      – tabela .route-params         → params (długość, czas, przewyższenie)
      – div .route-description       → description
      – div .gallery <img src=...>   → images (lista URL-i)
      – div #map                     → map embeds (lista tagów iframe lub podobnych)
      – div .user-review <p>…</p>    → reviews
    """

    def __init__(self):
        super().__init__()
        self.reset_state()

    def reset_state(self):
        # parsowanie tabeli parametrów
        self.in_params_table = False
        self.in_td           = False
        self.td_count        = 0
        self.current_key     = None
        self.buffer          = ""
        self.params          = {}

        # opis trasy
        self.in_desc_div        = False
        self.description_parts  = []

        # galeria zdjęć
        self.in_gallery      = False
        self.images          = []

        # mapa interaktywna
        self.in_map_div      = False
        self.map_embeds      = []

        # recenzje użytkowników
        self.in_review_div   = False
        self.in_review_p     = False
        self.current_review  = ""
        self.reviews         = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # tabela parametrów
        if tag == "table" and attrs.get("class") == "route-params":
            self.in_params_table = True
        if self.in_params_table and tag == "td":
            self.in_td    = True
            self.td_count += 1
            self.buffer   = ""

        # opis trasy
        if tag == "div" and attrs.get("class") == "route-description":
            self.in_desc_div = True

        # galeria
        if tag == "div" and attrs.get("class") == "gallery":
            self.in_gallery = True
        if self.in_gallery and tag == "img" and attrs.get("src"):
            self.images.append(attrs["src"])

        # mapa
        if tag == "div" and attrs.get("id") == "map":
            self.in_map_div = True
        # wejdźmy też do iframe wewnątrz mapy
        if self.in_map_div and tag == "iframe" and attrs.get("src"):
            self.map_embeds.append(attrs["src"])

        # recenzje
        if tag == "div" and attrs.get("class") == "user-review":
            self.in_review_div = True
        if self.in_review_div and tag == "p":
            self.in_review_p    = True
            self.current_review = ""

    def handle_data(self, data):
        if self.in_td:
            self.buffer += data
        if self.in_desc_div:
            self.description_parts.append(data)
        if self.in_review_p:
            self.current_review += data

    def handle_endtag(self, tag):
        # koniec pola <td>
        if tag == "td" and self.in_td:
            text = self.buffer.strip()
            if self.td_count % 2 == 1:
                # nazwa parametru
                self.current_key = text.rstrip(":").lower()
            else:
                # wartość parametru
                self.params[self.current_key] = text
            self.in_td = False

        # koniec tabeli parametrów
        if tag == "table" and self.in_params_table:
            self.in_params_table = False

        # koniec bloku opisu
        if tag == "div" and self.in_desc_div:
            self.in_desc_div = False

        # koniec galerii
        if tag == "div" and self.in_gallery:
            self.in_gallery = False

        # koniec mapy
        if tag == "div" and self.in_map_div:
            self.in_map_div = False

        # koniec akapitu recenzji
        if tag == "p" and self.in_review_p:
            self.reviews.append(self.current_review.strip())
            self.in_review_p = False

        # koniec bloku recenzji
        if tag == "div" and self.in_review_div:
            self.in_review_div = False

    def extract_all(self) -> dict:
        """
        Zwraca:
          {
            'params':       {...},
            'description':  'pełny opis...',
            'images':       ['url1', 'url2', ...],
            'map_embeds':   ['iframe_src1', ...],
            'reviews':      ['rev1', 'rev2', ...]
          }
        """
        desc = " ".join(p.strip() for p in self.description_parts if p.strip())
        return {
            "params":      self.params,
            "description": desc,
            "images":      self.images,
            "map_embeds":  self.map_embeds,
            "reviews":     self.reviews
        }


# --- Test wewnętrzny ---

if __name__ == "__main__":
    # podstaw ścieżkę do HTML, który chcesz przetestować
    with open("../../tests/test2.html", encoding="utf-8") as f:
        html = f.read()

    # 2. Utwórz parser i wgraj do niego HTML
    parser = HTMLRouteExtractor()
    parser.feed(html)
    parser.close()  # kończymy wczytywanie

    # 3. Wywołaj extract_all bez argumentów
    result = parser.extract_all()

    # 4. Pokaż rezultat
    print("Parametry trasy: ", result["params"])
    print("Opis:            ", result["description"])
    print("Obrazy:          ", result["images"])
    print("Mapy:            ", result["map_embeds"])
    print("Recenzje:        ", result["reviews"])
