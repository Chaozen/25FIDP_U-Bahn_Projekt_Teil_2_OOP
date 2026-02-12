from difflib import SequenceMatcher


def text_normalisieren(text, ersetzungen=None):
    """
    Normalisiert einen Eingabe-String für den Vergleich.

    Schritte:
    1. Entfernt Leerzeichen am Anfang/Ende.
    2. Wandelt alles in Kleinbuchstaben um (casefold: ß -> ss).
    3. Ersetzt Umlaute (ä->ae, ö->oe, ü->ue).
    4. Vereinheitlicht Sonderzeichen (Bindestriche zu Leerzeichen).
    5. Ersetzt gängige Abkürzungen wortweise (Mapping).

    Args:
        text (str): Der zu normalisierende Text.
        ersetzungen (dict, optional): Ein Dictionary mit Abkürzungen (Key)
                                      und deren Langform (Value).
                                      Falls None, werden Standard-U-Bahn-Kürzel genutzt.

    Returns:
        str: Der bereinigte Text oder ein leerer String, falls Input leer war.
    """
    if not text:
        return ""

    text = text.strip().casefold()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("-", " ")

    if ersetzungen is None:
        ersetzungen = {
            "hbf.": "hauptbahnhof", "hbf": "hauptbahnhof",
            "str.": "strasse", "str": "strasse"
        }

    einzelne_woerter = text.split()
    ergebnis_liste = []
    for wort in einzelne_woerter:
        if wort in ersetzungen:
            ergebnis_liste.append(ersetzungen[wort])
        else:
            ergebnis_liste.append(wort)

    return " ".join(ergebnis_liste)


from difflib import SequenceMatcher


def finde_aehnliche_station(eingabe_normalisiert, liste_original_namen):
    """
        Findet die am besten passende Station basierend auf einer (unscharfen) Eingabe.

        Schritte:
        1. Durchläuft alle Originalnamen der vorhandenen Stationen.
        2. Normalisiert jeden Originalnamen temporär für den Vergleich.
        3. Berechnet die Ähnlichkeit (Ratio) zwischen Eingabe und Stationsname.
        4. Prüft, ob die Ähnlichkeit die geforderte 80 %-Hürde erreicht.

        Args:
            eingabe_normalisiert (str): Der bereits durch text_normalisieren() bereinigte User-Input.
            liste_original_namen (list): Eine Liste der echten Stationsnamen (z.B. ["Fürth Hbf.", "Messe"]).

        Returns:
            str: Der optisch korrekte Originalname der Station, falls eine Übereinstimmung
                 >= 80 % gefunden wurde, andernfalls None.
        """
    beste_uebereinstimmung = None
    hoechster_wert = 0.0

    for original_name in liste_original_namen:
        # Wir normalisieren den Kandidaten nur zum VERGLEICHEN
        name_zum_vergleich = text_normalisieren(original_name)

        aehnlichkeit = SequenceMatcher(None, eingabe_normalisiert, name_zum_vergleich).ratio()

        if aehnlichkeit > hoechster_wert:
            hoechster_wert = aehnlichkeit
            beste_uebereinstimmung = original_name

    # 80% Hürde laut Backlog
    if hoechster_wert >= 0.8:
        return beste_uebereinstimmung
    return None