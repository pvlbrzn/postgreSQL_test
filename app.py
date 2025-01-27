from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os

# Создание объекта Flask
app = Flask(__name__)

# Настройки для подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pavel:pavel@localhost:5432/pavel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях в базе данных
app.config['SECRET_KEY'] = os.urandom(24)

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Инициализация Flask-Migrate
migrate = Migrate(app, db)


# Модели базы данных
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)


# Формы
class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Добавить рецепт')


# Главная страница
@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)


# Детали
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Логика для отображения рецепта по ID
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)


# Форма для добавления рецепта
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Рецепт добавлен.')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', form=form)


# Удаление рецепта
@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Рецепт удален.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание таблиц в PostgreSQL
    app.run(debug=True)
