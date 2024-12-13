from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random, db_config

app = Flask(__name__)

# Настройка пути к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///test.db"
db = SQLAlchemy(app)

# Модель User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    tg_acc = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

#Модель slots
class Slots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(120), unique=False, nullable=False)
    booker = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % self.name

# Роут для главной страницы
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Роут для добавления пользователя
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    tg_acc = request.form.get('tg_acc')
    if name and tg_acc:
        new_user = User(name=name, tg_acc=tg_acc)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

# Роут для удаления пользователя
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))
@app.route('/calendar')
def calendar():
    return render_template('Booking_calendar.html')

# Пример данных слотов
slots_data_1 = [
    {"time": "08:00 - 09:00", "booked": False},
    {"time": "09:00 - 10:00", "booked": True},
    {"time": "10:00 - 11:00", "booked": False},
]
slots_data_2 = [
    {"time": "13:00 - 14:00", "booked": False},
    {"time": "15:00 - 16:00", "booked": True},
    {"time": "17:00 - 18:00", "booked": False},
]
slots_data_3 = [
    {"time": "11:00 - 12:00", "booked": True},
    {"time": "12:00 - 13:00", "booked": False},
    {"time": "19:00 - 20:00", "booked": True},
    {"time": "21:00 - 22:00", "booked": False},
]


@app.route('/api/slots', methods=['GET'])
def get_slots():
    date_str = request.args.get('date')
    try:
        # Преобразуем строку в дату (если формат правильный)
        requested_date = datetime.fromisoformat(date_str)
        sl = random.choice([slots_data_1, slots_data_2, slots_data_3])
        # Получаем слоты из базы данных
        slots_json = db_config.get_available_slots(requested_date)

        # Возвращаем данные напрямую как JSON-ответ
        return jsonify(sl)
    except (ValueError, TypeError) as e:
        return jsonify({"Error": str(e)}), 400

# Создаём таблицы
with app.app_context():
    db.create_all()
    print("Таблицы созданы")

# Проверка и создание базы данных
if __name__ == '__main__':

# Запуск приложения
    app.run(debug=True)