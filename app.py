from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
from db import db
from models import Recipe, Ingredient, Reqs
from sqlalchemy import asc
from utils import save_instructions_to_json
import searchRecipe as s

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages
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
    print(param, filterType)
    recipes = s.searchFunc(request.args.get('query'), filterType, param)
    print(recipes)
    return render_template('list.html', recipes=recipes)

@app.route('/recipes/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('recipeName')
        instructions_list = request.form.getlist('instructionsList')
        instructions_text = '\n'.join(instructions_list)  # Convert list to string for DB

        cuisine = request.form.get('cuisineType')
        cook_time = request.form.get('time')
        difficulty = request.form.get('diff')

        # Create and store recipe in database
        new_recipe = Recipe(
            title=title,
            instructions=instructions_text,
            cuisine=cuisine,
            cook_time=int(cook_time) if cook_time else None,
            difficulty=difficulty
        )
        db.session.add(new_recipe)
        db.session.commit()

        # Save full instruction list to JSON
        save_instructions_to_json(new_recipe.id, instructions_list)

        ingredient_names = request.form.getlist('ingredientNames')
        amounts = request.form.getlist('amount')

        seen = set()
        for name, qty in zip(ingredient_names, amounts):
            if name and qty:
                ingredient = Ingredient.query.filter_by(name=name).first()
                if ingredient and ingredient.id not in seen:
                    req = Reqs(recipe_id=new_recipe.id, ingredient_id=ingredient.id, qty=int(qty))
                    db.session.add(req)
                    seen.add(ingredient.id)

        db.session.commit()
        flash(f"Recipe '{title}' created successfully!")
        return redirect(url_for('home'))


    if request.method == 'GET':
        ingredientsList = Ingredient.query.order_by(asc(Ingredient.name)).all()
        return render_template('create.html', ingredientsList=ingredientsList)

@app.route('/recipes/<int:id>')
def recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

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

@app.route('/recipes/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    # Delete any ingredient-recipe associations in Reqs
    Reqs.query.filter_by(recipe_id=id).delete()

    # Delete related instructions from JSON 
    try:
        import json
        with open('instructions.json', 'r') as f:
            data = json.load(f)
        data.pop(str(recipe.id), None)
        with open('instructions.json', 'w') as f:
            json.dump(data, f, indent=4)
    except:
        pass  

    # Delete the recipe itself
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5555)
