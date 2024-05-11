from repository import EventRepository


def addEventTeilnehmer(event_id, teilnehmer):
    EventRepository.add_event_teilnehmer(event_id, teilnehmer)


def showEventTeilnehmer(teilnehmer_id):
    return EventRepository.get_event_teilnehmer_by_id(teilnehmer_id)


def getAllEvents():
    return EventRepository.get_all_events()
