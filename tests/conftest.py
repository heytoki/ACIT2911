import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from pathlib import Path
from app import app
from db import db
from models import Recipe, Ingredient, Reqs, Comments

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up a test database once for all tests."""
    # Use an in-memory database for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False
    
    # Create the test database and context
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture
def client():
    """Create a test client for the Flask app with fresh test data."""
    # Create clean test data for each test
    with app.app_context():
        _create_test_data()
    
    # Return a test client
    with app.test_client() as client:
        yield client
    
    # Clean up test data after each test
    with app.app_context():
        _clear_test_data()

def _create_test_data():
    """Create test data for the database."""
    # Create ingredients
    ingredients = [
        Ingredient(name="Tomato", measure="piece"),
        Ingredient(name="Pasta", measure="gram"),
        Ingredient(name="Garlic", measure="clove"),
        Ingredient(name="Onion", measure="piece"),
        Ingredient(name="Olive Oil", measure="tablespoon")
    ]
    
    for ingredient in ingredients:
        db.session.add(ingredient)
    db.session.commit()
    
    # Create recipes
    recipes = [
        Recipe(
            title="Pasta with Tomato Sauce",
            instructions="1. Cook pasta\n2. Make sauce\n3. Mix together",
            cuisine="Italian",
            cook_time=30,
            difficulty="Easy"
        ),
        Recipe(
            title="Garlic Bread",
            instructions="1. Slice bread\n2. Add garlic butter\n3. Toast",
            cuisine="Italian",
            cook_time=15,
            difficulty="Easy"
        )
    ]
    
    for recipe in recipes:
        db.session.add(recipe)
    db.session.commit()
    
    # Create recipe-ingredient relationships
    requirements = [
        Reqs(recipe_id=1, ingredient_id=1, qty=3),  # Tomatoes for pasta
        Reqs(recipe_id=1, ingredient_id=2, qty=200),  # Pasta
        Reqs(recipe_id=1, ingredient_id=3, qty=2),  # Garlic for pasta
        Reqs(recipe_id=2, ingredient_id=3, qty=4),  # Garlic for bread
        Reqs(recipe_id=2, ingredient_id=5, qty=2)   # Olive oil for bread
    ]
    
    for req in requirements:
        db.session.add(req)
    
    # Create some comments
    comments = [
        Comments(recipe_id=1, author="John", commentPost="Delicious recipe!"),
        Comments(recipe_id=1, author="Alice", commentPost="I added some basil, made it even better!"),
        Comments(recipe_id=2, author="Bob", commentPost="Super easy and tasty!")
    ]
    
    for comment in comments:
        db.session.add(comment)
    
    db.session.commit()
    
    # Create instructions.json file
    instructions_data = {
        "1": ["Cook pasta", "Make sauce", "Mix together"],
        "2": ["Slice bread", "Add garlic butter", "Toast"]
    }
    
    # Ensure test directory structure exists
    test_dir = Path(app.instance_path)
    test_dir.mkdir(exist_ok=True)
    
    # Write instructions JSON
    try:
        with open('instructions.json', 'w') as f:
            import json
            json.dump(instructions_data, f, indent=4)
    except Exception as e:
        print(f"Error creating instructions.json: {e}")

def _clear_test_data():
    """Clear all test data."""
    db.session.query(Comments).delete()
    db.session.query(Reqs).delete()
    db.session.query(Recipe).delete()
    db.session.query(Ingredient).delete()
    db.session.commit()