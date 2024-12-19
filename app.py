from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from datetime import datetime
import click

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///booking_system.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Models
class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    booked = db.Column(db.Integer, nullable = False,default=0)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    slot = db.relationship('Slot', backref=db.backref('bookings', cascade="all, delete"))
    service = db.relationship('Service')


# Routes
@app.route('/')
def index():
    return render_template('Booking_calendar.html')


@app.route('/api/dates', methods=['GET'])
def get_dates():
    today = datetime.today().date()
    dates = Slot.query.with_entities(Slot.date).distinct().filter(Slot.date >= today).all()
    if not dates:
        return jsonify({"message": "No available slots."}), 404
    return jsonify([date[0].isoformat() for date in dates])


@app.route('/api/slots', methods=['GET'])
def get_slots():
    date_str = request.args.get('date')
    try:
        requested_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        slots = Slot.query.filter_by(date=requested_date).all()
        if not slots:
            return jsonify({"message": "No available slots for this date."}), 404

        print([
            {"id": slot.id, "time": slot.time, "booked": slot.booked, "date": slot.date}
            for slot in slots
        ])

        return jsonify([
            {"id": slot.id, "time": slot.time, "booked": slot.booked}
            for slot in slots
        ])
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400


@app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([
        {"id": service.id, "name": service.name}
        for service in services
    ])


@app.route('/api/book', methods=['POST'])
def book_slot():
    data = request.json
    slot_id = data.get('slot_id')
    service_id = data.get('service_id')

    slot = Slot.query.get(slot_id)
    if not slot or slot.booked:
        return jsonify({"error": "Slot not available."}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found."}), 404

    booking = Booking(slot=slot, service=service)
    slot.booked = True
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking successful."})


# Database initialization
@click.command("init-db")
@with_appcontext
def init_db():
    """Инициализация базы данных с дефолтными данными."""
    db.create_all()
    if not Service.query.first():
        default_services = ["Haircut", "Styling", "Coloring"]
        for service_name in default_services:
            db.session.add(Service(name=service_name))
        db.session.commit()
    print("Database initialized.")


# Регистрация команды Flask CLI
app.cli.add_command(init_db)

if __name__ == '__main__':
    app.run(debug=True)