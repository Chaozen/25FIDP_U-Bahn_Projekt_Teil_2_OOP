from datetime import datetime
from haltestellen import stationen
from ubahn import LinieU1
from preislogik import PreisLogik
from utils import text_normalisieren
from utils import finde_aehnliche_station

def main():
    u1 = LinieU1(stationen)
    preislogik = PreisLogik()

    # ----------------------------
    # Benutzereingaben
    # ----------------------------
    #start = input("Start-Haltestelle: ")
    #ziel = input("Ziel-Haltestelle: ")
    alle_stationen_namen = [s.name for s in u1.stationen]

    # --- SCHLEIFE FÜR DEN START ---
    while True:
        start_raw = input("Start-Haltestelle: ")
        start_normalisiert = text_normalisieren(start_raw)

        # Fuzzy-Suche prüft auf 80% Übereinstimmung
        start_name = finde_aehnliche_station(start_normalisiert, alle_stationen_namen)

        if start_name:
            # Falls eine Station gefunden wurde, speichern wir sie und brechen die Schleife ab
            start = start_name
            print(f"Gefunden: {start}")
            break
        else:
            print("Fehler: Unbekannte Station. Bitte versuchen Sie es erneut.")

    # --- SCHLEIFE FÜR DAS ZIEL ---
    while True:
        ziel_raw = input("Ziel-Haltestelle: ")
        ziel_normalisiert = text_normalisieren(ziel_raw)

        # Auch hier: Fuzzy-Suche für Tippfehler
        ziel_name = finde_aehnliche_station(ziel_normalisiert, alle_stationen_namen)

        if ziel_name:
            ziel = ziel_name
            print(f"Gefunden: {ziel}")
            break
        else:
            print("Fehler: Unbekannte Station. Bitte versuchen Sie es erneut.")

    # Ab hier geht dein Programm mit den Variablen 'start' und 'ziel' weiter...
    zeit = input("Früheste Abfahrtszeit (HH:MM): ")


    ermaessigung = input("Ermäßigung (Ja/Nein): ").lower()
    barzahlung = input("Barzahlung (Ja/Nein): ").lower()
    einzelfahrt = input("Einzelfahrt (Ja/Nein): ").lower()

    try:
        # ----------------------------
        # Nächste Abfahrt (liefert Minuten seit 00:00)
        # ----------------------------
        abfahrt_min = u1.naechste_abfahrt(start, ziel, zeit)

        # ----------------------------
        # Ankunft berechnen (liefert Minuten seit 00:00)
        # ----------------------------
        ankunft_min = u1.ankunftszeit(start, ziel, abfahrt_min)

        # ----------------------------
        # Formatieren in HH:MM
        # ----------------------------
        ankunft_rund = int(ankunft_min + 0.5)
        abfahrt_str = f"{int(abfahrt_min // 60):02d}:{int(abfahrt_min % 60):02d}"
        ankunft_str = f"{int(ankunft_rund // 60):02d}:{int(ankunft_rund % 60):02d}"

        # ----------------------------
        # Formatieren in HH:MM:SS für TESTzwecke
        # ----------------------------
        # Wir holen uns den Nachkommateil der Minuten (z.B. 0.5) und rechnen ihn mal 60
        # abfahrt_sekunden = int((abfahrt_min % 1) * 60)
        # ankunft_sekunden = int((ankunft_min % 1) * 60)
        #
        # abfahrt_str = f"{int(abfahrt_min // 60):02d}:{int(abfahrt_min % 60):02d}:{abfahrt_sekunden:02d}"
        # ankunft_str = f"{int(ankunft_min // 60):02d}:{int(ankunft_min % 60):02d}:{ankunft_sekunden:02d}"

        # ----------------------------
        # Ticket & Preis berechnen
        # ----------------------------
        ticket = preislogik.ticket_typ(start, ziel, stationen)
        preis = preislogik.berechne_preis(ticket, ermaessigung, barzahlung, einzelfahrt)

        # ----------------------------
        # Zeitstempel
        # ----------------------------
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # ----------------------------
        # Ausgabe
        # ----------------------------
        print("\n--- Verbindung ---")
        print(f"Zeitstempel: {timestamp}")
        print(f"Abfahrt:  {abfahrt_str}")
        print(f"Ankunft:  {ankunft_str}")
        print(f"Ticket:   {ticket}")
        print(f"Preis:    {preis:.2f} €")

    except ValueError as e:
        print("Fehler:", e)


if __name__ == "__main__":
    main()