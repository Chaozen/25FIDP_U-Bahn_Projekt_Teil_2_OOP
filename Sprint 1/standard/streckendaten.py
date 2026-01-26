"""
Modul: streckendaten.py
Beschreibung: gewichtete Adjazenzliste bildet Fahrtstrecke benachbarter Stationen und Fahrtzeit ab,
inklusive Betriebszeit und Abfahrtsintervallen
"""


# --- DATENBASIS ---

# 1. Die physische Strecke (Das Netz)
STRECKEN_NETZ = {
    "A": [("B", 2)],
    "B": [("C", 3)],
    "C": [("D", 1)],
    "D": []
}

# 2. Die Regeln (Der Takt und die Zeiten)
TAKT_KONFIGURATION = {
    "start_zeit": "05:00",  # Erster Zug ab Startbahnhof
    "ende_zeit": "23:00",   # Letzter Zug ab Startbahnhof
    "takt_minuten": 10      # Alle X Minuten
}