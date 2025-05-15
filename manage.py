from db import db
from models import Recipe, Ingredient, Reqs
from app import create_app

app = create_app()

def drop_all():
    with app.app_context():
        db.drop_all()
        print("All tables dropped.")

def create_all():
    with app.app_context():
        db.create_all()
        print("All tables created.")

def add_recipes():
    sample_data = {
        "Spaghetti Bolognese": {
            "instructions": "1. Cook pasta\n2. Prepare sauce\n3. Mix and serve",
            "ingredients": ["Spaghetti", "Tomato sauce", "Ground beef"],
            "cuisine": "italian",
            "cook_time": 30,
            "difficulty": "medium"
        },
        "Pancakes": {
            "instructions": "1. Mix ingredients\n2. Pour batter\n3. Flip and serve",
            "ingredients": ["Flour", "Milk", "Eggs"],
            "cuisine": "american",
            "cook_time": 15,
            "difficulty": "easy"
        },
        "Chicken Curry": {
            "instructions": "1. Sauté onions\n2. Add spices and chicken\n3. Simmer with coconut milk",
            "ingredients": ["Chicken", "Onions", "Spices", "Coconut milk"],
            "cuisine": "indian",
            "cook_time": 40,
            "difficulty": "hard"
        },
        "Sushi Rolls": {
            "instructions": "1. Prepare rice\n2. Add fillings\n3. Roll and slice",
            "ingredients": ["Sushi rice", "Nori", "Fish", "Vegetables"],
            "cuisine": "japanese",
            "cook_time": 50,
            "difficulty": "hard"
        },
        "Tacos": {
            "instructions": "1. Prepare fillings\n2. Heat tortillas\n3. Assemble tacos",
            "ingredients": ["Tortillas", "Beef", "Lettuce", "Cheese"],
            "cuisine": "mexican",
            "cook_time": 25,
            "difficulty": "medium"
        },
        "Greek Salad": {
            "instructions": "1. Chop vegetables\n2. Add feta and olives\n3. Drizzle with olive oil",
            "ingredients": ["Tomatoes", "Cucumber", "Feta", "Olives", "Olive oil"],
            "cuisine": "greek",
            "cook_time": 10,
            "difficulty": "easy"
        }
    }

    with app.app_context():
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
                ingredient = Ingredient.query.filter_by(name=item).first()
                if not ingredient:
                    ingredient = Ingredient(name=item, measure="unit")
                    db.session.add(ingredient)
                    db.session.commit()

                req = Reqs(recipe_id=recipe.id, ingredient_id=ingredient.id, qty=1)
                db.session.add(req)
            db.session.commit()

        print("Sample recipes added.")

def clear_recipes():
    with app.app_context():
        db.session.query(Reqs).delete()
        db.session.query(Ingredient).delete()
        db.session.query(Recipe).delete()
        db.session.commit()
        print("All recipes, ingredients, and requirements deleted.")

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
