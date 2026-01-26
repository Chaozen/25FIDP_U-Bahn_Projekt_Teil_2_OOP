"""
Modul: data.py
Beschreibung: Erstellt die konkreten Objekte für unser U-Bahn-Netz.
"""
# Wir brauchen unsere neuen Klassen
from models import Strecke

# Die Konfiguration (Takt) bleibt ein einfaches Dictionary (das ist okay so)
TAKT_KONFIGURATION = {
    "start_zeit": "05:00",
    "ende_zeit": "23:00",
    "takt_minuten": 10
}

def erstelle_demo_strecke():
    """
    Erstellt die Instanz der Strecke und baut die Stationen A-B-C-D auf.
    Gibt das fertige Strecken-Objekt zurück.
    """
    # 1. Die leere Strecke erstellen
    bahn = Strecke()

    # 2. Die Stationen erstellen (die Strecke merkt sie sich intern)
    a = bahn.add_station("A")
    b = bahn.add_station("B")
    c = bahn.add_station("C")
    d = bahn.add_station("D")

    # 3. Die Verbindungen knüpfen (Objekt zu Objekt)
    # A -> B (2 Min)
    a.add_nachbar(b, 2)

    # B -> C (3 Min)
    b.add_nachbar(c, 3)

    # C -> D (1 Min)
    c.add_nachbar(d, 1)

    # Das fertige Netz zurückgeben
    return bahn