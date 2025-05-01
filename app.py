from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from db import db
from models import Recipe, Ingredient
import json
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

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
        ingredients_text = request.form.get('ingredients')  # multiple lines
        instructions_text = request.form.get('instructions')  # optional

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

# --- Utility function to save instructions in a JSON file ---
def save_instructions_to_json(recipe_id, instructions_text):
    instructions_file = "instructions.json"
    steps = [line.strip() for line in instructions_text.strip().split('\n') if line.strip()]

    if os.path.exists(instructions_file):
        with open(instructions_file, 'r') as f:
            try:
                data = json.load(f)
            except ValueError:
                data = {}
    else:
        data = {}

    data[str(recipe_id)] = steps

    with open(instructions_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True, port=5555)
