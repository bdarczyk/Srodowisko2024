import json

def load_config(path="config.json"):
    """
    Wczytuje plik konfiguracyjny JSON.

    path: Ścieżka do pliku konfiguracyjnego (domyślnie 'config.json')
    return: Słownik z konfiguracją lub pusty słownik przy błędzie
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd wczytywania konfiguracji: {e}")
        return {}

def update_budget_limit(category, new_limit, config_path="config.json"):
    """
    Aktualizuje lub dodaje limit budżetowy dla podanej kategorii w pliku konfiguracyjnym.

    category: Nazwa kategorii
    new_limit: Nowy limit dla tej kategorii
    config_path: Ścieżka do pliku konfiguracyjnego (domyślnie 'config.json')
    return True, jeśli zapis zakończy się sukcesem
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}
    budgets = config.get("budgets", {})
    budgets[category] = new_limit
    config["budgets"] = budgets
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    return True
