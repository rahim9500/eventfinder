from flask import render_template
from repository.EventRepository import get_event_by_id
from repository import KategorieRepository


def showEvent(event_id, is_authorized):
    event = get_event_by_id(event_id)
    all_kategorien = KategorieRepository.get_all_kategorien()
    if event:
        return render_template(
            "eventSingle.html",
            event=event,
            all_kategorien=all_kategorien,
            is_authorized=is_authorized,
        )
    else:
        return render_template("event_not_found.html")
