import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app
import pytest
from models import Recipe, Ingredient, Reqs

# test homepage, ensure it has test recipe name in it
def test_homepage_accessible():
    app.config['TESTING'] = True
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    assert b'Pancakes' in res.data


def test_new_recipe():
    """
    GIVEN a Recipe model
    WHEN a new Recipe is created
    THEN check that the fields are correctly initialized
    """
    recipe = Recipe(title="Pancakes", instructions="Mix ingredients and cook", cuisine="American", cook_time=10, difficulty="Easy")
    
    assert recipe.title == "Pancakes"
    assert recipe.instructions == "Mix ingredients and cook"
    assert recipe.cuisine == "American"
    assert recipe.cook_time == 10
    assert recipe.difficulty == "Easy"


def test_new_ingredient():
    """
    GIVEN an Ingredient model
    WHEN a new Ingredient is created
    THEN check that the fields are correctly initialized
    """
    ingredient = Ingredient(name="Flour", measure="cups")
    
    assert ingredient.name == "Flour"
    assert ingredient.measure == "cups"


def test_new_req():
    """
    GIVEN a Reqs model
    WHEN a new Reqs entry is created linking Recipe and Ingredient
    THEN check that the relationship and fields are correctly initialized
    """
    recipe = Recipe(title="Pancakes", instructions="Mix ingredients and cook", cuisine="American", cook_time=10, difficulty="Easy")
    ingredient = Ingredient(name="Flour", measure="cups")
    req = Reqs(recipe_id=1, ingredient_id=1, qty=2)

    assert req.recipe_id == 1
    assert req.ingredient_id == 1
    assert req.qty == 2

