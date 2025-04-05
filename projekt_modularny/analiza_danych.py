from functools import reduce

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

def oblicz_statystyki_pogody(pogoda):
    srednia_temp = list(map(lambda maks, min: (maks + min) / 2, pogoda["maks_temp"], pogoda["min_temp"]))
    suma_opadow = reduce(lambda suma, opad: suma + opad, pogoda["opady"], 0)
    dni_sloneczne = reduce(lambda suma, godziny: suma + (1 if godziny > 5 else 0), pogoda["godziny_sloneczne"], 0)
    return {
        "srednia_temp": srednia_temp,
        "suma_opadow": suma_opadow,
        "dni_sloneczne": dni_sloneczne
    }

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

def filtruj_trasy(trasy, min_dlugosc, max_dlugosc, trudnosc, teren, region):
    return list(filter (
        lambda trasa:(min_dlugosc <= trasa['dlugosc_km'] <= max_dlugosc)
        and (trudnosc is None or trasa['trudnosc'] == trudnosc)
        and (teren is None or trasa['typ_terenu'] == teren)
        and (region is None or trasa['region'].lower() == region.lower()), trasy)
    )