# --- LOGIK TEIL B: Komfortfunktionen ---

def validiere_station(eingabe_str, offsets_dict):
    """
    Nimmt den User-Input entgegen, macht ihn groß (upper) und prüft, ob er existiert.
    Gibt den sauberen Stationsnamen zurück (oder None).
    """
    if not eingabe_str:
        return None

    # .upper() lässt akzeptiert kleinschreibung bei Input
    # .strip() entfernt Leerzeichen, falls der User versehentlich " A " eingibt.
    bereinigte_eingabe = eingabe_str.strip().upper()

    if bereinigte_eingabe in offsets_dict:
        return bereinigte_eingabe
    else:
        return None

def uhrzeit_zu_minuten(zeit_str):
    """
    LÖSUNG ZU FRAGE 2:
    Macht die Eingabe robust gegen Punkt statt Doppelpunkt.
    """
    zeit_str = zeit_str.strip()

    # Hier erlauben wir den Punkt: "08.00" wird zu "08:00"
    zeit_str = zeit_str.replace('.', ':')

    if ':' not in zeit_str and len(zeit_str) == 3:
        zeit_str = '0' + zeit_str

    # Hier erlauben wir fehlende Trennzeichen: "0800" wird zu "08:00"
    if ':' not in zeit_str and len(zeit_str) == 4:
        zeit_str = zeit_str[:2] + ':' + zeit_str[2:]

    try:
        parts = zeit_str.split(':')
        stunden = int(parts[0])
        minuten = int(parts[1])
        return stunden * 60 + minuten
    except (ValueError, IndexError):
        # Bei Quatsch-Eingaben geben wir -1 zurück (Fehlercode)
        return -1

def minuten_zu_uhrzeit(minuten_wert):
    stunden = (minuten_wert // 60) % 24
    minuten = minuten_wert % 60
    return f"{stunden:02d}:{minuten:02d}"