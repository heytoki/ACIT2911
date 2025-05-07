from db import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    cuisine = db.Column(db.String(50))
    cook_time = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    measure = db.Column(db.String(), nullable=False)

class Reqs(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    db.PrimaryKeyConstraint(
        recipe_id, ingredient_id
    )
    qty = db.Column(db.Integer)