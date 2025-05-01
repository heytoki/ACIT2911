from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from db import db
from models import Recipe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
db.init_app(app)

with app.app_context():
    db.create_all()  # create tables if they don't exist

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes')
def list():
    return render_template('list.html')

@app.route('/recipes/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')

        new_recipe = Recipe(title=title, ingredients=ingredients)
        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('create.html')

@app.route('/recipes/recipe')
def recipe():
    return render_template('recipe.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
