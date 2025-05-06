from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from db import db
from models import Recipe, Ingredient
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
    recipes = s.searchFunc(request.args.get('query'))
    return render_template('list.html', recipes=recipes)

@app.route('/recipes/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients_text = request.form.get('ingredients')  
        instructions_text = request.form.get('instructions') 

        # Create recipe
        new_recipe = Recipe(title=title, instructions=instructions_text)
        db.session.add(new_recipe)
        db.session.commit()

        # Create ingredient entries
        ingredients = ingredients_text.strip().split('\n')
        for item in ingredients:
            if item.strip():
                db.session.add(Ingredient(name=item.strip(), recipe_id=new_recipe.id))

        db.session.commit()

        # Save instructions to JSON file (optional)
        save_instructions_to_json(new_recipe.id, instructions_text)

        return redirect(url_for('home'))

    return render_template('create.html')

@app.route('/recipes/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/ingredient')
def ingredient():
    return render_template('ingredient.html')


if __name__ == '__main__':
    app.run(debug=True, port=5555)
