# Event Finder

**Event Finder** is a web application to search for events. <br />
**Participents** can search for events and apply for which they like <br />
**Searchers** can create events and manage them.

## Installation and Run

- Clone the repository:
  ```bash
  git clone https://git.mylab.th-luebeck.de/swt1/eventfinder.git
  ```
  ```bash
   cd eventfinder
  ```
- _Create a virtual environment (recommended):_
  ```bash
  python3 -m venv venv
  ```
- _Activate the virtual environment (skip this step if you didn't create a virtual environment):_
  ```bash
  source venv/bin/activate
  # On Windows use `venv\Scripts\activate`
  ```
- Install the dependencies:
  ```bash
   pip install -r requirements.txt
  ```
- edit in config/.env:
  ```bash
   add your Mail and password
  ```
- Run the application:
  ```bash
   python3 app.py
   # On Windows use `python app.py`
  ```
- finally open a browser and go to http://127.0.0.1:5000 to access the application.

## Usage

- As a searcher

  - Go to the home page and click on the 'Event Erstellen' button.
  - Fill in the form and click on the 'Event Erstellen' button.
  - You will be redirected to the home page where you can see your event after you confim the email that has been sent to you.
  - You can edit or delete your event by clicking on the 'Bearbeiten' or 'Löschen' Links that will be send after confirmation.

* As a participant
  - Go to the home page where you can see the Events.
    - Click on an event to see the details.
    - Call the number that is displayed to confirm your participation.
    - Your participation will be displayed on the event page.
  - You can also filter the events by category, age group, location, date and number of contanstencs, to find the event that best suits you.

* Administrating Categories
  - Visit the route "/administrator/categories"
  - Click on a category to see the details.
    - Edit the categories name or delete a category
  - Click on "Kategorie erstellen" to create a new category
  

## Technologies used

- Flask: Python web framework for building web applications.
- SQLAlchemy: Python SQL toolkit and Object Relational Mapper.
- HTML, CSS, JavaScript: Frontend technologies.
  - Bootstrap: CSS framework for developing responsive websites.

## Contributing

- Jacob Weinhold
- Jonas Wegner
- Rakhim Khasukhanov
- Yannick Maschke
- Sailesh Upreti
- Samer Al-Haj Hemidi

## License

[TH Lübeck](https://www.th-luebeck.de/)
