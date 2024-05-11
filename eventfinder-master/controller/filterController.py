from datetime import datetime
from repository import EventRepository

# from model.alter import Alter


def filter_events(
    kategorien, altergruppe, ort, datum_von, datum_bis, teilnehmer_anzahl
):
    return __passes_filter(
        kategorien, altergruppe, ort, datum_von, datum_bis, teilnehmer_anzahl
    )


def __passes_filter(
    kategorien, altergruppe, ort, datum_von, datum_bis, teilnehmer_anzahl
):
    datum_von = datetime.strptime(datum_von, "%Y-%m-%d").date()
    datum_bis = datetime.strptime(datum_bis, "%Y-%m-%d").date()

    events = EventRepository.get_all_events()
    filtered_events = []

    for event in events:
        if (
            (event.ort == ort)
            and event.altersgruppe.name == altergruppe
            and (event.datum >= datum_von and event.datum <= datum_bis)
            and (
                teilnehmer_anzahl - 10
                <= event.gesuchte_teilnehmer_anzahl
                <= teilnehmer_anzahl + 10
            )
        ):
            for selected_Kategorie in kategorien:
                for kategorie in event.kategorien:
                    if kategorie.name == selected_Kategorie:
                        filtered_events.append(event)
    return filtered_events
