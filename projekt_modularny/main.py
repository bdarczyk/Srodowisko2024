from odczyt_zapis_danych import odczyt_plikow, zapisz_rekomendacje, zapisz_rekomendacje_pogodowe
from analiza_danych import (
    przetworz_plik_pogoda,
    przetworz_plik_trasy,
    filtruj_trasy,
    filtruj_dni_na_wyprawe
)

def main():
    plik_pogoda, plik_trasy = odczyt_plikow()
    przetworzona_pogoda = przetworz_plik_pogoda(plik_pogoda)
    przetworzone_trasy = przetworz_plik_trasy(plik_trasy)

    min_dlugosc = float(input("Podaj minimalną długość trasy (km): "))
    max_dlugosc = float(input("Podaj maksymalną długość trasy (km): "))
    trudnosc = input("Podaj poziom trudności (1-5 lub Enter by pominąć): ")
    trudnosc = int(trudnosc) if trudnosc.isdigit() else None
    teren = input("Podaj typ terenu (urban, forest, mountain, etc.) lub Enter by pominąć: ") or None
    region = input("Podaj region lub Enter by pominąć: ") or None

    przefiltrowane_trasy = filtruj_trasy(przetworzone_trasy, min_dlugosc, max_dlugosc, trudnosc, teren, region)
    zapisz_rekomendacje(przefiltrowane_trasy)

    min_temp = float(input("Minimalna średnia temperatura (°C): "))
    max_temp = float(input("Maksymalna średnia temperatura (°C): "))
    min_slonce = float(input("Minimalna liczba godzin słońca: "))
    max_opady = float(input("Maksymalna ilość opadów (mm): "))

    rekomendacje_pogodowe = filtruj_dni_na_wyprawe(przetworzona_pogoda, min_temp, max_temp, min_slonce, max_opady)
    zapisz_rekomendacje_pogodowe(rekomendacje_pogodowe)

if __name__ == "__main__":
    main()
