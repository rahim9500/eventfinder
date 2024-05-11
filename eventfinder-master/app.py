# --------------------- External Imports ----------------------- #
import os
from flask import (
    request,
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
)
from dotenv import load_dotenv
from pathlib import Path
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

# --------------------- Internal Imports ----------------------- #
from model.suchender import Suchender
from model.teilnehmer import Teilnehmer
from model.event import Event
from model.kategorie import Kategorie
from model.alter import Alter
from model.status import Status
from repository.extension import db
from repository import KategorieRepository, EventRepository
from controller import eventController, filterController, categoryController
from view import eventView, categoryView

# --------------------- Database and App Initialization ----------------------- #
# App initialization
app = Flask(__name__)
load_dotenv(Path("config/.env"))
app.secret_key = os.getenv("SECRET_KEY")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

# E-Mail Server configuration
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


# ------------------------------------------------------------------------------ #


# ------------------------------- Routes --------------------------------------- #


# Homepage route
@app.route("/")
@app.route("/home")
def home():
    list_of_kategorien = allKategorien()
    list_of_events = allEvents()
    return render_template(
        "homepage.html", events=list_of_events, list_of_categories=list_of_kategorien
    )


# Erstellen seite route
@app.route("/erstellenseite")
def erstellenseite():
    list_of_kategorien = allKategorien()
    return render_template("create.html", kategorien=list_of_kategorien)


# facebook route
@app.route("/facebook")
def facebook():
    return redirect("https://www.facebook.com/")


# twitter route
@app.route("/twitter")
def twitter():
    return redirect("https://twitter.com/")


# Alle Events als liste zurückgeben
def allEvents():
    return eventController.getAllEvents()


# Alle Kategorien als liste zurückgeben
def allKategorien():
    return KategorieRepository.get_all_kategorien()


# Ansicht aller vorhandenen Kategorien
@app.route("/administrator/categories", methods=["POST", "GET"])
def show_categories():
    list_of_kategorien = KategorieRepository.get_all_kategorien()
    return render_template("categories.html", kategorien=list_of_kategorien)


# Ansicht der Seite, die das Erstellen einer neuen Kategorie erlaubt
@app.route("/administrator/categories/create")
def create_category():
    return render_template("createCategory.html")


# Hinzufügen einer neuen Kategorie
@app.route("/administrator/categories/add/", methods=["POST"])
def add_category():
    kategorie_name = request.form['kategorieName']
    print(categoryController.create_category(kategorie_name))
    kategorien = KategorieRepository.get_all_kategorien()
    return render_template("categories.html", kategorien=kategorien)


# Löschen  einer Kategorie
@app.route("/administrator/categories/delete/<kategorie_name>", methods=["GET", "POST"])
def delete_category(kategorie_name):
    # kategorie_name = request.form['kategorieName']
    kategorie = KategorieRepository.get_kategorie_by_name(kategorie_name)
    categoryController.delete_category(kategorie.id)
    kategorien = KategorieRepository.get_all_kategorien()
    return render_template("categories.html", kategorien=kategorien)


# Bearbeiten einer Kategorie
@app.route("/administrator/categories/update/<old_kategorie_name>", methods=["POST"])
def update_category(old_kategorie_name):
    new_kategorie_name = request.form['kategorieName']
    old_kategorie = KategorieRepository.get_kategorie_by_name(old_kategorie_name)
    if new_kategorie_name == old_kategorie:
        kategorien = KategorieRepository.get_all_kategorien()
        return render_template("categories.html", kategorien=kategorien)
    categoryController.update_category(old_kategorie.id, new_kategorie_name)
    kategorien = KategorieRepository.get_all_kategorien()
    return render_template("categories.html", kategorien=kategorien)


# Ansicht einer einzelnen Kategorie
@app.route("/administrator/categorySingle/<kategorie_id>", methods=["GET"])
def categorySingle(kategorie_id):
    return categoryView.showCategory(kategorie_id)


# Filter route
@app.route("/filter", methods=["POST"])
def filter():
    list_of_kategorien = allKategorien()

    kategerien = request.form.getlist("kategory")
    altergruppe = request.form["ageGroup"]
    ort = request.form["ort"]
    date_from_str = request.form["date_from"]
    date_to_str = request.form["date_to"]
    if date_from_str and date_to_str:
        date_from_str = date_from_str.split("T")[0]
        date_to_str = date_to_str.split("T")[0]
        datum_von = datetime.strptime(date_from_str, "%Y-%m-%d")
        datum_bis = datetime.strptime(date_to_str, "%Y-%m-%d")
    else:
        datum_von = datetime.today()
        datum_bis = datetime.today()
    datum_von = datum_von.strftime("%Y-%m-%d")
    datum_bis = datum_bis.strftime("%Y-%m-%d")
    teilnehmer_anzahl = request.form.get("teilnehmer")
    if teilnehmer_anzahl == "" or teilnehmer_anzahl is None:
        teilnehmer_anzahl = 0
    else:
        teilnehmer_anzahl = int(teilnehmer_anzahl)

    filtered_events = filterController.filter_events(
        kategerien, altergruppe, ort, datum_von, datum_bis, teilnehmer_anzahl
    )
    return render_template(
        "homepage.html", events=filtered_events, list_of_categories=list_of_kategorien
    )


# Event erstellen route
@app.route("/erstellen", methods=["POST", "GET"])
def event_erstellen():
    if request.method == "POST":
        # Retrieve form data
        name = request.form["name"]
        dauer = int(request.form["dauer"])
        ort = request.form["ort"]
        datum = datetime.strptime(request.form["datum"], "%Y-%m-%d").date()
        uhrzeit = request.form["uhrzeit"]
        altersgruppe = request.form["altersgruppe"]
        preis = float(request.form["preis"])
        status = request.form["status"]
        gesuchte_teilnehmer_anzahl = int(request.form["gesuchte_teilnehmer_anzahl"])
        suchender_name = request.form["suchender_name"]
        suchender_nummer = request.form["suchender_nummer"]
        suchender_mail = request.form["suchender_mail"]
        kategorien = request.form.getlist("kategorien")

        if preis < 0:
            flash(
                "Preis/Dauer/Gesuchte Teilnehmer Anzahl darf nicht negativ sein.",
                "error",
            )
            return redirect(url_for("erstellen"))

        if dauer <= 0 or gesuchte_teilnehmer_anzahl <= 0:
            flash(
                "Dauer/Gesuchte Teilnehmer Anzahl darf nicht negativ oder 0 sein.",
                "error",
            )
            return redirect(url_for("erstellen"))

        kategorie_objekte = []
        verarbeitete_kategorien = set()

        for kategorie_name in kategorien:
            if kategorie_name not in verarbeitete_kategorien:
                vorhandene_kategorie = KategorieRepository.get_kategorie_by_name(
                    kategorie_name
                )
                if vorhandene_kategorie:
                    kategorie_objekte.append(vorhandene_kategorie)
                else:
                    neue_kategorie = Kategorie(name=kategorie_name)
                    KategorieRepository.add_kategorie(neue_kategorie)
                    kategorie_objekte.append(neue_kategorie)

                verarbeitete_kategorien.add(kategorie_name)

        new_event = Event(
            name=name,
            dauer=dauer,
            ort=ort,
            datum=datum,
            uhrzeit=uhrzeit,
            altersgruppe=altersgruppe,
            preis=preis,
            status=status,
            gesuchte_teilnehmer_anzahl=gesuchte_teilnehmer_anzahl,
            suchender=Suchender(suchender_name, suchender_mail, suchender_nummer),
            kategorien=kategorie_objekte,
            teilnehmer=[Teilnehmer(suchender_name)],
        )

        suchender = Suchender(suchender_name, suchender_mail, suchender_nummer)

        token = generate_confirmation_token(suchender_mail)

        new_event.confirmation_token = token

        session["event_draft"] = new_event.serialize()
        session["suchender_draft"] = suchender.serialize()

        send_confirmation_email(suchender_mail, token)

        if new_event.id:
            return redirect(url_for("eventSingle", event_id=new_event.id))
        else:
            flash("Fehler beim Erstellen des Events", "error")
            return redirect(url_for("home"))

    all_kategorien = KategorieRepository.get_all_kategorien()
    return render_template("create.html", kategorien=all_kategorien)


# ------------------------------------------------------------------------------ #


# Token-Generierungsfunktion
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt="email-confirmation-salt")


def send_confirmation_email(email, event_id):
    if "@" not in email or "." not in email.split("@")[1]:
        flash("Ungültige E-Mail-Adresse", "error")
        return
    token = generate_confirmation_token(email)
    confirm_url = url_for(
        "confirm_event_creation", event_id=event_id, token=token, _external=True
    )
    msg = Message(
        "Bitte bestätigen Sie Ihr Event",
        sender="rakhimtestflask@gmail.com",
        recipients=[email],
    )
    msg.body = f"Bitte klicken Sie auf den folgenden Link, um Ihr Event zu bestätigen: {confirm_url}"
    mail.send(msg)


def send_access_email(email, event_id):
    token = generate_confirmation_token(email)

    edit_url = url_for("edit_event", event_id=event_id, token=token, _external=True)
    delete_confirm_url = url_for(
        "confirm_delete", event_id=event_id, token=token, _external=True
    )
    add_participant_url = url_for(
        "add_participant", event_id=event_id, token=token, _external=True
    )

    msg = Message(
        "Verwalten Sie Ihr Event",
        sender="rakhimtestflask@gmail.com",
        recipients=[email],
    )
    msg.body = (
        f"Um Ihr Event zu bearbeiten, besuchen Sie bitte diesen Link: {edit_url}\n"
        f"Um Ihr Event zu löschen, besuchen Sie bitte diesen Link: {delete_confirm_url}\n"
        f"Um Teilnehmer zu Ihrem Event hinzuzufügen oder zu entfernen, besuchen Sie bitte diesen Link: {add_participant_url}"
    )

    mail.send(msg)


@app.route("/eventSingle/<int:event_id>", methods=["GET"])
def eventSingle(event_id):
    token = request.args.get("token", None)
    is_authorized = False

    if token:
        try:
            email = URLSafeTimedSerializer(app.secret_key).loads(
                token, salt="email-confirmation-salt", max_age=100000000000
            )
            event = EventRepository.get_event_by_id(event_id)
            if event and event.suchender.mail == email:
                is_authorized = True
        except Exception as e:
            flash(f"Fehler beim Laden des Events: {e}", "error")

    event = EventRepository.get_event_by_id(event_id)
    if not event:
        flash("Event nicht gefunden.", "danger")
        return render_template("event_not_found.html")
    return eventView.showEvent(event_id, is_authorized)


@app.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    token = request.args.get("token", None)
    all_kategorien = KategorieRepository.get_all_kategorien()

    if token is None:
        flash("Zugriff verweigert: Kein Token vorhanden.", "danger")
        return redirect(url_for("home"))

    try:
        email = URLSafeTimedSerializer(app.secret_key).loads(
            token, salt="email-confirmation-salt", max_age=3600
        )
    except Exception as e:
        flash(f"Fehler beim Laden des Events: {e}", "error")
        return redirect(url_for("home"))

    event = EventRepository.get_event_by_id(event_id)
    if not event or event.suchender.mail != email:
        flash(
            "Zugriff verweigert: Sie sind nicht berechtigt, dieses Event zu bearbeiten.",
            "danger",
        )
        return redirect(url_for("home"))

    if request.method == "POST":
        event.name = request.form.get("name", event.name)
        event.dauer = request.form.get("dauer", event.dauer)
        event.ort = request.form.get("ort", event.ort)
        event.datum = datetime.strptime(request.form["datum"], "%Y-%m-%d").date()
        event.uhrzeit = request.form.get("uhrzeit", event.uhrzeit)
        event.altersgruppe = Alter[request.form["altersgruppe"]]
        event.preis = request.form.get("preis", event.preis)
        event.status = Status[request.form["status"]]
        event.gesuchte_teilnehmer_anzahl = request.form.get(
            "gesuchte_teilnehmer_anzahl", event.gesuchte_teilnehmer_anzahl
        )
        suchender_name = request.form.get("suchender_name")
        suchender_telefon = request.form.get("suchender_nummer")

        # Aktualisieren Sie das Suchender-Objekt
        if event.suchender:
            event.suchender.name = suchender_name
            event.suchender.telefon = suchender_telefon

        if float(request.form["preis"]) < 0:
            flash(
                "Preis/Dauer/Gesuchte Teilnehmer Anzahl darf nicht negativ sein.",
                "error",
            )
            return redirect(url_for("edit_event", event_id=event_id))

        if (
                int(request.form["dauer"]) <= 0
                or int(request.form["gesuchte_teilnehmer_anzahl"]) <= 0
        ):
            flash(
                "Dauer/Gesuchte Teilnehmer Anzahl darf nicht negativ oder 0 sein.",
                "error",
            )
            return redirect(url_for("edit_event", event_id=event_id))

        event.kategorien = [
            KategorieRepository.get_kategorie_by_name(k)
            for k in request.form.getlist("kategorien")
        ]

        # Datenbankaktualisierung
        try:
            db.session.commit()
            flash("Event erfolgreich aktualisiert!", "success")
            return redirect(url_for("eventSingle", event_id=event_id, token=token))
        except Exception as e:
            db.session.rollback()
            flash(f"Fehler bei der Aktualisierung des Events: {e}", "error")
            return render_template(
                "edit.html", event=event, token=token, kategorien=all_kategorien
            )

    return render_template(
        "edit.html", event=event, token=token, kategorien=all_kategorien
    )


@app.route("/add_participant/<int:event_id>", methods=["GET", "POST"])
def add_participant(event_id):
    token = request.args.get("token")

    # Token-Überprüfung
    if not token:
        flash("Zugriff verweigert: Kein Token vorhanden.", "error")
        return redirect(url_for("home"))

    try:
        email = URLSafeTimedSerializer(app.secret_key).loads(
            token, salt="email-confirmation-salt", max_age=100000000000
        )
    except Exception as e:
        flash(f"Fehler beim Laden des Events: {e}", "error")
        return redirect(url_for("home"))

    event = EventRepository.get_event_by_id(event_id)
    if not event or event.suchender.mail != email:
        flash(
            "Zugriff verweigert: Sie sind nicht berechtigt, Teilnehmer hinzuzufügen.",
            "danger",
        )
        return redirect(url_for("home"))

    if request.method == "POST":
        if len(event.teilnehmer) >= event.gesuchte_teilnehmer_anzahl:
            flash("Maximale Teilnehmerzahl erreicht.", "error")
            return redirect(url_for("add_participant", event_id=event_id, token=token))

        participant_name = request.form.get("participant_name")
        if not participant_name:
            flash("Teilnehmername fehlt", "error")
            return redirect(url_for("add_participant", event_id=event_id, token=token))

        teilnehmer = Teilnehmer(name=participant_name)
        # Hinzufügen des Teilnehmers zum Event
        EventRepository.add_event_teilnehmer(event_id, teilnehmer)
        flash("Teilnehmer wurde hinzugefügt", "success")
        return redirect(url_for("eventSingle", event_id=event_id, token=token))

    return render_template(
        "add_participant.html", event=event, event_id=event_id, token=token
    )


@app.route("/remove_participant/<int:event_id>", methods=["POST"])
def remove_participant(event_id):
    token = request.form.get("token")
    participant_id = request.form.get("participant_id")

    if token is None or participant_id is None:
        flash("Fehlerhafte Anfrage.", "error")
        EventRepository.delete_event_teilnehmer_by_id(event_id, participant_id)
        return redirect(url_for("eventSingle", event_id=event_id))

    try:
        email = URLSafeTimedSerializer(app.secret_key).loads(
            token, salt="email-confirmation-salt", max_age=100000000000
        )
    except Exception as e:
        flash(f"Fehler beim entfernen des Teilnehmers: {e}", "error")
        return redirect(url_for("eventSingle", event_id=event_id))

    event = EventRepository.get_event_by_id(event_id)
    if not event or event.suchender.mail != email:
        flash(
            "Zugriff verweigert: Sie sind nicht berechtigt, Teilnehmer zu entfernen.",
            "danger",
        )
        return redirect(url_for("eventSingle", event_id=event_id))

    try:
        EventRepository.delete_event_teilnehmer_by_id(event_id, participant_id)
        flash("Teilnehmer erfolgreich entfernt", "success")
    except Exception as e:
        flash(f"Fehler beim Entfernen des Teilnehmers: {e}", "error")

    return redirect(url_for("eventSingle", event_id=event_id, token=token))


@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    token = request.args.get("token", None)

    if token is None:
        flash("Zugriff verweigert: Kein Token vorhanden.", "danger")
        return redirect(url_for("home"))

    try:
        email = URLSafeTimedSerializer(app.secret_key).loads(
            token, salt="email-confirmation-salt", max_age=100000000000
        )
    except Exception as e:
        flash(f"Fehler beim löschen des Events: {e}", "error")
        return redirect(url_for("home"))

    event = EventRepository.get_event_by_id(event_id)
    if not event or event.suchender.mail != email:
        flash(
            "Zugriff verweigert: Sie sind nicht berechtigt, dieses Event zu löschen.",
            "danger",
        )
        return redirect(url_for("home"))

    try:
        db.session.delete(event)
        db.session.commit()
        flash("Event erfolgreich gelöscht!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Löschen des Events: {e}", "error")

    return redirect(url_for("home"))


@app.route("/confirm_delete/<int:event_id>", methods=["GET"])
def confirm_delete(event_id):
    token = request.args.get("token", None)
    if token is None:
        flash("Zugriff verweigert: Kein Token vorhanden.", "danger")
        return redirect(url_for("home"))
    try:
        email = URLSafeTimedSerializer(app.secret_key).loads(
            token, salt="email-confirmation-salt", max_age=100000000000
        )
    except Exception as e:
        flash(f"Fehler beim Löschen des Events: {e}", "error")
        return redirect(url_for("home"))

    event = EventRepository.get_event_by_id(event_id)
    if not event or event.suchender.mail != email:
        flash(
            "Zugriff verweigert: Sie sind nicht berechtigt, dieses Event zu löschen.",
            "danger",
        )
        return redirect(url_for("home"))

    return render_template("confirm_delete.html", event_id=event_id, token=token)


@app.route("/confirm/<token>")
def confirm_event_creation(token):
    try:
        email = URLSafeTimedSerializer(app.secret_key).loads(
            token, salt="email-confirmation-salt", max_age=100000000000
        )
    except Exception as e:
        flash(f"Fehler beim Erstellen des Events: {e}", "error")
        return redirect(url_for("home"))

    event = EventRepository.get_event_by_token(token)

    if event:
        send_access_email(email, event.id, token)
        return redirect(url_for("eventSingle", event_id=event.id, token=token))

    event_draft = session.get("event_draft")
    suchender_draft = session.get("suchender_draft")

    if event_draft and suchender_draft:
        event = Event.deserialize(event_draft)
        suchender = Suchender.deserialize(suchender_draft)
        event.suchender = suchender

        EventRepository.add_event(event)
        session.pop("event_draft", None)
        session.pop("suchender_draft", None)

        send_access_email(email, event.id)
        flash("Ihr Event wurde erfolgreich erstellt!", "success")
        return redirect(url_for("eventSingle", event_id=event.id, token=token))

    else:
        flash(
            "Event-Entwurf nicht gefunden. Bitte erstellen Sie Ihr Event erneut.",
            "danger",
        )
        return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not KategorieRepository.get_kategorie_by_name("Art"):
            KategorieRepository.add_kategorie(kategorie=Kategorie("Art"))
        if not KategorieRepository.get_kategorie_by_name("Sport"):
            KategorieRepository.add_kategorie(kategorie=Kategorie("Sport"))
    app.run(debug=True)
