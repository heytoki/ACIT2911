from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from db import db
from models import Recipe, Ingredient
from sqlalchemy import asc
from utils import save_instructions_to_json
import searchRecipe as s

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"

# database location in the data folder
app.instance_path = Path("data").resolve()

db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)

@app.route('/recipes')
def list():
    filterType = request.args.get('filterType', default='title')
    param = request.args.get(filterType)
    recipes = s.searchFunc(request.args.get('query'), filterType, param)
    return render_template('list.html', recipes=recipes)

@app.route('/recipes/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('recipeName')
        ingredients_text = request.form.getlist('ingredientNames')
        instructions_text = request.form.getlist('instructionsList')

        # Create recipe
        new_recipe = Recipe(title=title, instructions=instructions_text)
        db.session.add(new_recipe)
        db.session.commit()

        # Create ingredient entries
        # ingredients = ingredients_text.strip().split('\n')
        # for item in ingredients:
        #     if item.strip():
        #         db.session.add(Ingredient(name=item.strip(), recipe_id=new_recipe.id))

        db.session.commit()

        # Save instructions to JSON file (optional)
        save_instructions_to_json(new_recipe.id, instructions_text)

        return redirect(url_for('home'))
    
    if request.method == 'GET':
        ingredientsList = Ingredient.query.order_by(asc(Ingredient.name)).all()
        return render_template('create.html', ingredientsList=ingredientsList)

@app.route('/recipes/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/ingredient', methods=['GET', 'POST'])
def ingredient():
    if request.method == 'GET':
        return render_template('ingredient.html')

    if request.method == 'POST':
        name = request.form.get('name')
        measure = request.form.to_dict()['measures']
        ingredient = Ingredient(name=name, measure=measure)
        db.session.add(ingredient)
        db.session.commit()
        return render_template('ingredient.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
