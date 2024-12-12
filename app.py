from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


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

# Создаём таблицы
with app.app_context():
    db.create_all()
    print("Таблицы созданы")

# Проверка и создание базы данных
if __name__ == '__main__':

# Запуск приложения
    app.run(debug=True)