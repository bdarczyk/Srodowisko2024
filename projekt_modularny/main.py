from odczyt_zapis_danych import odczyt_plikow, zapisz_rekomendacje, zapisz_statystyki
from analiza_danych import (
    przetworz_plik_pogoda,
    oblicz_statystyki_pogody,
    przetworz_plik_trasy,
    filtruj_trasy
)

def main():
    plik_pogoda, plik_trasy = odczyt_plikow()
    przetworzona_pogoda = przetworz_plik_pogoda(plik_pogoda)
    przetworzone_trasy = przetworz_plik_trasy(plik_trasy)
    statystyki_pogody = oblicz_statystyki_pogody(przetworzona_pogoda)

    min_dlugosc = float(input("Podaj minimalną długość trasy (km): "))
    max_dlugosc = float(input("Podaj maksymalną długość trasy (km): "))
    trudnosc = input("Podaj poziom trudności 1-5 lu wciśnij Enter by pominąć): ")
    trudnosc = int(trudnosc) if trudnosc.isdigit() else None
    teren = input("Podaj typ terenu (urban, forest, mountain, beach, park, mixed, valley, river, swamp, nature) lub naciśnij Enter by pominąć ") or None
    region = input("Podaj region lub wciśnij Enter by pominąć): ") or None

    przefiltrowane_trasy = filtruj_trasy(przetworzone_trasy, min_dlugosc, max_dlugosc, trudnosc, teren, region)

    zapisz_rekomendacje(przefiltrowane_trasy)
    zapisz_statystyki(statystyki_pogody)

if __name__ == "__main__":
    main()