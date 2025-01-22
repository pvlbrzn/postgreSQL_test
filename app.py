from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Создание объекта Flask
app = Flask(__name__)

# Настройки для подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pavel:pavel@localhost:5432/pavel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях в базе данных

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Инициализация Flask-Migrate
migrate = Migrate(app, db)


# Пример модели (таблицы) для работы с данными
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


@app.route('/')
def index():
    new_user = User(username="john_doe", email="john@example.com")
    db.session.add(new_user)
    db.session.commit()
    return (("Пользователь создан"))


@app.route('/all')
def all():
    users = User.query.all()
    for user in users:
        print(user.username, user.email)
    return ("все пользователи")


if __name__ == '__main__':
    app.run(debug=True)
