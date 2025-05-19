from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
from db import db
from models import Recipe, Ingredient, Reqs, Comments
from sqlalchemy import asc
from utils import save_instructions_to_json
import searchRecipe as s
import json

def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
    app.instance_path = Path("data").resolve()

    if config:
        app.config.update(config)

    db.init_app(app)

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
            instructions_list = request.form.getlist('instructionsList')
            instructions_text = '\n'.join(instructions_list)

            cuisine = request.form.get('cuisineType')
            cook_time = request.form.get('time')
            difficulty = request.form.get('diff')

            new_recipe = Recipe(
                title=title,
                instructions=instructions_text,
                cuisine=cuisine,
                cook_time=int(cook_time) if cook_time else None,
                difficulty=difficulty
            )
            db.session.add(new_recipe)
            db.session.commit()

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

        ingredientsList = Ingredient.query.order_by(asc(Ingredient.name)).all()
        return render_template('create.html', ingredientsList=ingredientsList)

    @app.route('/recipes/<int:id>', methods=['GET', 'POST'])
    def recipe(id):
        recipe = db.session.get(Recipe, id)
        if not recipe:
            return "Recipe not found", 404

        if request.method == 'POST':
            author = request.form.get('author')
            commentPost = request.form.getlist('commentPost')
            commentPost = '\n'.join(commentPost)
            comment = Comments(author=author, commentPost=commentPost, recipe_id=id)
            db.session.add(comment)
            db.session.commit()

        commentList = Comments.query.filter(Comments.recipe_id == id).limit(10)
        return render_template('recipe.html', recipe=recipe, commentList=commentList)

    @app.route('/ingredient', methods=['GET', 'POST'])
    def ingredient():
        if request.method == 'POST':
            name = request.form.get('name')
            measure = request.form.to_dict().get('measures')
            if name and measure:
                ingredient = Ingredient(name=name, measure=measure)
                db.session.add(ingredient)
                db.session.commit()
                flash(f"Ingredient '{name}' added successfully!")
            return redirect(url_for('ingredient'))

        return render_template('ingredient.html')


    @app.route('/recipes/delete/<int:id>', methods=['POST'])
    def delete_recipe(id):
        recipe = db.session.get(Recipe, id)
        if not recipe:
            return "Recipe not found", 404

        Reqs.query.filter_by(recipe_id=id).delete()

        try:
            with open('instructions.json', 'r') as f:
                data = json.load(f)
            data.pop(str(recipe.id), None)
            with open('instructions.json', 'w') as f:
                json.dump(data, f, indent=4)
        except:
            pass

        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted successfully!")
        return redirect(url_for('home'))

    @app.route('/comments/delete/<int:comment_id>/<int:recipe_id>', methods=['POST'])
    def delete_comment(comment_id, recipe_id):
        comment = db.session.get(Comments, comment_id)
        if not comment:
            return "Comment not found", 404

        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted.")
        return redirect(url_for('recipe', id=recipe_id))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)
