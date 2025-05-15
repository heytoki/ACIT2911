import pytest
from app import create_app
from db import db
from models import Recipe, Ingredient, Reqs, Comments

@pytest.fixture
def app_context():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    with app.app_context():
        db.create_all()
        yield app

def test_create_recipe(app_context):
    recipe = Recipe(title="Toast", instructions="Toast bread", cuisine="other", cook_time=3, difficulty="easy")
    db.session.add(recipe)
    db.session.commit()
    assert Recipe.query.count() == 1

def test_create_ingredient(app_context):
    ingredient = Ingredient(name="Bread", measure="slice")
    db.session.add(ingredient)
    db.session.commit()
    assert Ingredient.query.count() == 1

def test_recipe_ingredient_link(app_context):
    recipe = Recipe(title="Toast", instructions="Toast bread", cuisine="other", cook_time=3, difficulty="easy")
    ingredient = Ingredient(name="Bread", measure="slice")
    db.session.add_all([recipe, ingredient])
    db.session.commit()

    req = Reqs(recipe_id=recipe.id, ingredient_id=ingredient.id, qty=2)
    db.session.add(req)
    db.session.commit()

    assert Reqs.query.count() == 1

def test_create_comment(app_context):
    recipe = Recipe(title="Toast", instructions="Toast bread", cuisine="other", cook_time=3, difficulty="easy")
    db.session.add(recipe)
    db.session.commit()

    comment = Comments(author="TestUser", commentPost="Looks good", recipe_id=recipe.id)
    db.session.add(comment)
    db.session.commit()

    assert Comments.query.count() == 1
