import json

def odczyt_plikow():
    with open('dane/pogoda.json', 'r', encoding="utf-8") as plik_pogoda:
        plik_pogoda = json.load(plik_pogoda)
    with open('dane/trasy.json', 'r', encoding="utf-8") as plik_trasy:
        plik_trasy = json.load(plik_trasy)
    return plik_pogoda, plik_trasy

def zapisz_rekomendacje(rekomendowane_trasy):
    with open('rekomendowane_trasy.json', 'w', encoding="utf-8") as plik:
        json.dump(rekomendowane_trasy, plik, indent=4, ensure_ascii=False)

def zapisz_rekomendacje_pogodowe(dni):
    with open("dogodne_dni.json", "w", encoding="utf-8") as plik:
        json.dump(dni, plik, indent=4, ensure_ascii=False)
