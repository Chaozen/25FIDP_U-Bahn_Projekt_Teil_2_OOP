class Station:
    def __init__(self, name, fahrzeit_zur_naechsten):
        self.name = name
        self.fahrzeit_zur_naechsten = fahrzeit_zur_naechsten  # Minuten


class LinieU1:
    def __init__(self, stationen, takt=10):
        self.stationen = stationen
        self.takt = takt  # Minuten
        self.startzeit = 5 * 60      # 05:00
        self.endzeit = 23 * 60       # 23:00

        self.hauptknoten = {"Plärrer", "Hauptbahnhof"}
        self.endstationen = {stationen[0].name, stationen[-1].name}

    def haltezeit(self, station):
        if station.name in self.hauptknoten:
            return 1.0
        if station.name in self.endstationen:
            return 1.0
        return 0.5

    def generiere_fahrplan(self):
        fahrplan = {s.name: [] for s in self.stationen}

        for zugstart in range(self.startzeit, self.endzeit + 1, self.takt):
            # ------------------
            # Hinfahrt (+1)
            # ------------------
            zeit = zugstart
            for i, station in enumerate(self.stationen):
                fahrplan[station.name].append((zeit, +1))
                zeit += self.haltezeit(station)
                if i < len(self.stationen) - 1:
                    zeit += station.fahrzeit_zur_naechsten

            # Wendezeit
            # zeit += 1.0 # todo : zeit 0 oder 1 (0 ist OK, Sven hat getestet)

            # ------------------
            # Rückfahrt (-1)
            # ------------------
            for i in range(len(self.stationen) - 1, -1, -1):
                station = self.stationen[i]
                fahrplan[station.name].append((zeit, -1))
                zeit += self.haltezeit(station)
                if i > 0:
                    zeit += self.stationen[i - 1].fahrzeit_zur_naechsten

        return fahrplan

    def naechste_abfahrt(self, start, ziel, uhrzeit):
        stunden, minuten = map(int, uhrzeit.split(":"))
        wunsch = stunden * 60 + minuten

        fahrplan = self.generiere_fahrplan()

        if start not in fahrplan or ziel not in fahrplan:
            raise ValueError("Unbekannte Station.")

        indices = {s.name: i for i, s in enumerate(self.stationen)}

        if indices[start] == indices[ziel]:
            raise ValueError("Start und Ziel sind identisch.")

        # gewünschte Richtung bestimmen
        richtung = 1 if indices[ziel] > indices[start] else -1

        # nur Abfahrten mit passender Richtung UND Zeit >= Wunschzeit
        kandidaten = [
            zeit for zeit, r in fahrplan[start]
            if r == richtung and zeit >= wunsch
        ]

        if not kandidaten:
            raise ValueError("Keine Bahn mehr heute.")

        beste = min(kandidaten)
        return f"{int(beste // 60):02d}:{int(beste % 60):02d}"


# ----------------------------
# U1 Daten
# ----------------------------


# a = Langwasser Süd
# b = Gemeinschaftshaus
u1_daten = [
    ("Langwasser Süd", 3),
    ("Gemeinschaftshaus", 2),
    ("Langwasser Mitte", 2),
    ("Scharfreiterring", 3),
    ("Langwasser Nord", 2),
    ("Messe", 3),
    ("Bauernfeindstraße", 2),
    ("Hasenbuck", 2),
    ("Frankenstraße", 2),
    ("Maffeiplatz", 1),
    ("Aufseßplatz", 2),
    ("Hauptbahnhof", 2),
    ("Lorenzkirche", 3),
    ("Weißer Turm", 2),
    ("Plärrer", 2),
    ("Gostenhof", 1),
    ("Bärenschanze", 2),
    ("Maximilianstraße", 2),
    ("Eberhardshof", 2),
    ("Muggenhof", 3),
    ("Stadtgrenze", 2),
    ("Jakobinenstraße", 3),
    ("Fürth Hbf", 0)
]
# c = Jakobinenstraße
# d = Fürth Hbf


stationen = [Station(name, zeit) for name, zeit in u1_daten]
u1 = LinieU1(stationen)

# ----------------------------
# Benutzereingabe
# ----------------------------

start = input("Start-Haltestelle: ")
ziel = input("Ziel-Haltestelle: ")
zeit = input("Früheste Abfahrtszeit (HH:MM): ")


# Test
# print('\n Test: von Langwasser Mitte zur Messe und ist um 05:01 Uhr am Bahnsteig. \n Ergebnis: Das System hat 05:06 Uhr als Abfahrtszeit berechnet.\n')
# start = "Langwasser Mitte" # input("Start-Haltestelle: ")
# ziel = "Messe" # input("Ziel-Haltestelle: ")
# zeit = "05:01" # input("Früheste Abfahrtszeit (HH:MM): ")


try:
    abfahrt = u1.naechste_abfahrt(start, ziel, zeit)
    print(f"Nächste Abfahrt ab {start}: {abfahrt}")
except ValueError as e:
    print("Fehler:", e)


if __name__ == "__main__":
    linie1 = LinieU1(stationen)