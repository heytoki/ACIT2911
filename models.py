from db import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    measure = db.Column(db.String(), nullable=False)

class Reqs(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    qty = db.Column(db.Integer)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    author = db.Column(db.String(100), nullable=False)
    commentPost = db.Column(db.String(), nullable=False)