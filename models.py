from db import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    cuisine = db.Column(db.String(50))
    cook_time = db.Column(db.String)
    difficulty = db.Column(db.String(20))

    ingredients = db.relationship("Ingredient", backref="recipe", lazy=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
