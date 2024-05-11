from flask import render_template
from repository import KategorieRepository


def showCategory(kategorie_id):
    kategorie = KategorieRepository.get_kategorie_by_id(kategorie_id)
    if kategorie:
        return render_template(
            "categorySingle.html", kategorie=kategorie
        )
    else:
        return render_template("event_not_found.html")
