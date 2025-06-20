import logging

def setup_logger():
    """
    Konfiguruje system logowania aplikacji.

    Tworzy plik 'app.log', ustawia poziom logowania na INFO
    oraz definiuje format logów (czas, poziom, wiadomość).
    Loguje komunikat startowy po uruchomieniu aplikacji.
    """
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Aplikacja uruchomiona")
