"""
Modul: main.py
Beschreibung: User Interface (OOP-Version).
Hier nutzen wir jetzt das Strecken-Objekt statt der losen Funktionen.
"""

# Wir importieren die Konfiguration UND unsere neue "Bau-Funktion"
from streckendaten import TAKT_KONFIGURATION, erstelle_demo_strecke

# utils ist nur noch für Helfer-Tools (Zeit/Validierung) da
import utils

def main():
    # --- 1. INITIALISIERUNG (Das Netz erwacht zum Leben) ---
    print("System startet... baue Streckennetz (OOP)...")

    # NEU: Wir holen uns das fertige Objekt aus der Fabrik-Funktion
    u_bahn_netz = erstelle_demo_strecke()

    # NEU: Wir fragen das Objekt nach den Fahrzeiten
    # Syntax: objekt.methode()
    offsets = u_bahn_netz.berechne_offsets("A")

    # --- 2. USER INPUT (Wie gehabt) ---
    print("\n--- FAHRPLANAUSKUNFT (OOP v1.0) ---")

    raw_input_station = input("An welcher Haltestelle stehen Sie? (A, B, C, D): ")

    # Validierung über das Helfer-Modul
    start_haltestelle = utils.validiere_station(raw_input_station, offsets)

    if start_haltestelle is None:
        print(f"Fehler: Die Station '{raw_input_station}' kennen wir leider nicht.")
        return

    raw_input_zeit = input("Ab welcher Uhrzeit wollen Sie fahren? (z.B. 08:00): ")
    wunsch_minuten = utils.uhrzeit_zu_minuten(raw_input_zeit)

    if wunsch_minuten == -1:
        print("Fehler: Ungültiges Zeitformat.")
        return

    # --- 3. SUCHE (Wie gehabt) ---
    # Da wir 'offsets' jetzt vom Objekt bekommen haben, funktioniert der Rest exakt gleich!

    offset_station = offsets[start_haltestelle]
    start_betrieb = utils.uhrzeit_zu_minuten(TAKT_KONFIGURATION["start_zeit"])
    ende_betrieb = utils.uhrzeit_zu_minuten(TAKT_KONFIGURATION["ende_zeit"])
    takt = TAKT_KONFIGURATION["takt_minuten"]

    zug_gefunden = False

    for abfahrt_in_a in range(start_betrieb, ende_betrieb + 1, takt):
        real_abfahrt = abfahrt_in_a + offset_station

        if real_abfahrt >= wunsch_minuten:
            zeit_str = utils.minuten_zu_uhrzeit(real_abfahrt)
            print(f"Der nächste Zug fährt um {zeit_str} Uhr ab.")
            zug_gefunden = True
            break

    if not zug_gefunden:
        print("Heute fährt leider kein Zug mehr.")

if __name__ == "__main__":
    main()