import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
import json
from pathlib import Path
from app import app
from db import db
from models import Recipe, Ingredient, Reqs, Comments

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    # Create the test database
    with app.app_context():
        db.create_all()
        # Create test data
        _create_test_data()
        
    # Return a test client
    with app.test_client() as client:
        yield client
    
    # Clean up after test
    with app.app_context():
        db.drop_all()

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
    with open('instructions.json', 'w') as f:
        json.dump(instructions_data, f, indent=4)


# Test home page
def test_home_page(client):
    """Test that the home page loads and displays recipes."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Pasta with Tomato Sauce' in response.data
    assert b'Garlic Bread' in response.data


def test_recipe_search(client):
    """Test searching for recipes."""
    response = client.get('/recipes?query=Pasta&filterType=title')
    assert response.status_code == 200
    assert b'Pasta with Tomato Sauce' in response.data
    assert b'Garlic Bread' not in response.data


def test_recipe_detail_nonexistent(client):
    """Test requesting a non-existent recipe."""
    response = client.get('/recipes/999')
    assert response.status_code == 404


# Test creating a recipe
def test_create_recipe_form(client):
    """Test that the create recipe form loads."""
    response = client.get('/recipes/create')
    assert response.status_code == 200
    assert b'Create New Recipe' in response.data
    assert b'Recipe Name' in response.data


def test_create_recipe(client):
    """Test creating a new recipe."""
    response = client.post('/recipes/create', data={
        'recipeName': 'Chocolate Cake',
        'instructionsList': [
            'Mix dry ingredients', 
            'Add wet ingredients', 
            'Bake at 350F for 30 minutes'
        ],
        'cuisineType': 'Dessert',
        'time': '45',
        'diff': 'Medium',
        'ingredientNames': ['Flour', 'Sugar'],
        'amount': ['2', '1']
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Check that the recipe was added to the database
    with app.app_context():
        recipe = Recipe.query.filter_by(title='Chocolate Cake').first()
        assert recipe is not None
        assert recipe.cuisine == 'Dessert'
        assert recipe.cook_time == 45
        assert recipe.difficulty == 'Medium'


# Test adding comments to a recipe
def test_add_comment(client):
    """Test adding a comment to a recipe."""
    response = client.post('/recipes/1', data={
        'author': 'TestUser',
        'commentPost': ['This is a test comment']
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'TestUser' in response.data
    assert b'This is a test comment' in response.data
    
    # Check that the comment was added to the database
    with app.app_context():
        comment = Comments.query.filter_by(author='TestUser').first()
        assert comment is not None
        assert comment.commentPost == 'This is a test comment'
        assert comment.recipe_id == 1


# Test adding an ingredient
def test_add_ingredient(client):
    """Test adding a new ingredient."""
    response = client.post('/ingredient', data={
        'name': 'Chocolate',
        'measures': 'gram'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Check that the ingredient was added to the database
    with app.app_context():
        ingredient = Ingredient.query.filter_by(name='Chocolate').first()
        assert ingredient is not None
        assert ingredient.measure == 'gram'


# Test deleting a recipe
def test_delete_recipe(client):
    """Test deleting a recipe."""
    response = client.post('/recipes/delete/1', follow_redirects=True)
    assert response.status_code == 200
    
    # Check that the recipe is no longer on the home page
    assert b'Pasta with Tomato Sauce' not in response.data
    
    # Check that the recipe was removed from the database
    with app.app_context():
        recipe = Recipe.query.filter_by(id=1).first()
        assert recipe is None
        
        # Check that associated requirements were also deleted
        reqs = Reqs.query.filter_by(recipe_id=1).all()
        assert len(reqs) == 0