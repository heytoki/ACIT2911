# manage.py
# Just to add sample data into our databse and manage it for testing
from db import db
from models import Recipe, Ingredient
from app import app
import json

def drop_all():
    db.drop_all()
    print("All tables dropped.")

def create_all():
    db.create_all()
    print("All tables created.")

def add_recipes():
    sample_data = {
        "Spaghetti Bolognese": {
            "instructions": "1. Cook pasta\n2. Prepare sauce\n3. Mix and serve",
            "ingredients": ["Spaghetti", "Tomato sauce", "Ground beef"],
            "cuisine": "Italian",
            "cook_time": 30,
            "difficulty": "Medium"
        },
        "Pancakes": {
            "instructions": "1. Mix ingredients\n2. Pour batter\n3. Flip and serve",
            "ingredients": ["Flour", "Milk", "Eggs"],
            "cuisine": "American",
            "cook_time": 15,
            "difficulty": "Easy"
        },
        "Chicken Curry": {
            "instructions": "1. Sauté onions\n2. Add spices and chicken\n3. Simmer with coconut milk",
            "ingredients": ["Chicken", "Onions", "Spices", "Coconut milk"],
            "cuisine": "Indian",
            "cook_time": 40,
            "difficulty": "Hard"
        },
        "Sushi Rolls": {
            "instructions": "1. Prepare rice\n2. Add fillings\n3. Roll and slice",
            "ingredients": ["Sushi rice", "Nori", "Fish", "Vegetables"],
            "cuisine": "Japanese",
            "cook_time": 50,
            "difficulty": "Hard"
        },
        "Tacos": {
            "instructions": "1. Prepare fillings\n2. Heat tortillas\n3. Assemble tacos",
            "ingredients": ["Tortillas", "Beef", "Lettuce", "Cheese"],
            "cuisine": "Mexican",
            "cook_time": 25,
            "difficulty": "Medium"
        },
        "Greek Salad": {
            "instructions": "1. Chop vegetables\n2. Add feta and olives\n3. Drizzle with olive oil",
            "ingredients": ["Tomatoes", "Cucumber", "Feta", "Olives", "Olive oil"],
            "cuisine": "Greek",
            "cook_time": 10,
            "difficulty": "Easy"
        }
    }



    for title, data in sample_data.items():
        recipe = Recipe(
            title=title,
            instructions=data["instructions"],
            cuisine=data["cuisine"],
            cook_time=data["cook_time"],
            difficulty=data["difficulty"]
        )
        db.session.add(recipe)
        db.session.commit()

        for item in data["ingredients"]:
            db.session.add(Ingredient(name=item, recipe_id=recipe.id))
        db.session.commit()



    print("Sample recipes added")

def clear_recipes():
    Ingredient.query.delete()
    Recipe.query.delete()
    db.session.commit()
    print("All recipes and ingredients deleted.")


if __name__ == "__main__":
    with app.app_context():
        command = input("Enter command (add, clear, drop, create): ").strip()

        if command == "add":
            add_recipes()
        elif command == "clear":
            clear_recipes()
        elif command == "drop":
            drop_all()
        elif command == "create":
            create_all()
        else:
            print("Invalid command")

