"""
Modul: models.py
Beschreibung: Definition der Klassen (Baupläne) für Stationen und das Netz.
"""


class Station:
    """Repräsentiert einen einzelnen Haltepunkt."""

    def __init__(self, name):
        # Das hier passiert, wenn wir eine Station erstellen:
        self.name = name

        # Jede Station hat ihre eigene Liste mit Nachbarn.
        # Vorher war das im großen Dictionary, jetzt trägt es die Station selbst.
        self.nachbarn = []

    def add_nachbar(self, andere_station, fahrzeit):
        """Merkt sich eine Verbindung zu einer anderen Station."""
        # Wir speichern das ganze Objekt 'andere_station', nicht nur den Namen string!
        verbindung = (andere_station, fahrzeit)
        self.nachbarn.append(verbindung)


class Strecke:
    """Der Manager für das gesamte Netz."""

    def __init__(self):
        # Ein Verzeichnis, um Stationen per Namen zu finden
        # z.B. {"A": <StationObjekt A>, "B": <StationObjekt B>}
        self.stationen = {}

    def add_station(self, name):
        """Erstellt eine neue Station und legt sie im Verzeichnis ab."""
        neue_station = Station(name)
        self.stationen[name] = neue_station
        return neue_station

    def berechne_offsets(self, start_name):
        """
        Diese Logik kennst du! Sie ist aus 'utils.py' hierher umgezogen.
        Der Unterschied: Wir arbeiten jetzt mit Objekten statt Strings.
        """
        offsets = {}

        # 1. Start-Objekt holen
        if start_name not in self.stationen:
            return {}  # Leeres Ergebnis bei Fehler

        current_station = self.stationen[start_name]
        current_time = 0

        # Start eintragen
        offsets[current_station.name] = current_time

        # Solange die Station Nachbarn hat
        while current_station.nachbarn:
            # 1. Daten holen
            # Da wir OOP nutzen, bekommen wir hier direkt das nächste Station-OBJEKT
            nachste_station_obj, fahrzeit = current_station.nachbarn[0]

            # 2. Zeit aktualisieren
            current_time = current_time + fahrzeit

            # 3. Ergebnis speichern
            offsets[nachste_station_obj.name] = current_time

            # 4. Zeiger weiterschieben (wir springen auf das nächste Objekt)
            current_station = nachste_station_obj

        return offsets