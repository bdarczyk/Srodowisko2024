from functools import reduce

def przetworz_plik_trasy(plik_trasy):
    return list(map(lambda trasa: {
        'id': trasa['id'],
        'nazwa': trasa['name'],
        'region': trasa['region'],
        'dlugosc_km': trasa['length_km'],
        'trudnosc': trasa['difficulty'],
        'typ_terenu': trasa['terrain_type'],
        'tagi': trasa['tags']
    }, plik_trasy))

def przetworz_plik_pogoda(plik_pogoda):
    dzien = plik_pogoda['daily']
    godziny_sloneczne = list(map(lambda czas: czas / 3600, dzien['sunshine_duration']))
    return {
        "daty": dzien['time'],
        "godziny_sloneczne": godziny_sloneczne,
        "maks_temp": dzien['temperature_2m_max'],
        "min_temp": dzien['temperature_2m_min'],
        "opady": dzien['precipitation_sum'],
        "zachmurzenie": dzien['cloudcover_mean']
    }

def filtruj_trasy(trasy, min_dlugosc, max_dlugosc, trudnosc, teren, region):
    return list(filter(
        lambda trasa: (
            min_dlugosc <= trasa['dlugosc_km'] <= max_dlugosc and
            (trudnosc is None or trasa['trudnosc'] == trudnosc) and
            (teren is None or trasa['typ_terenu'] == teren) and
            (region is None or trasa['region'].lower() == region.lower())
        ), trasy))

def filtruj_dni_na_wyprawe(pogoda, min_temp, max_temp, min_slonce, max_opady):
    return list(filter(
        lambda dzien: (
            min_temp <= dzien["srednia_temp"] <= max_temp and
            dzien["slonce_godz"] >= min_slonce and
            dzien["opady_mm"] <= max_opady
        ),
        map(
            lambda i: {
                "data": pogoda["daty"][i],
                "srednia_temp": pogoda["maks_temp"][i] + pogoda["min_temp"][i],
                "slonce_godz": pogoda["godziny_sloneczne"][i],
                "opady_mm": pogoda["opady"][i]
            },
            range(len(pogoda["daty"]))
        )
    ))

