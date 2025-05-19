import pytest
from app import create_app
from db import db
from models import Recipe, Ingredient, Comments

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_recipe_post(client):
    with client.application.app_context():
        flour = Ingredient(name="Flour", measure="cup")
        db.session.add(flour)
        db.session.commit()

    form_data = {
        'recipeName': 'Test Cake',
        'cuisineType': 'other',
        'time': '10',
        'diff': 'easy',
        'ingredientNames': 'Flour',
        'amount': '1',
        'instructionsList': 'Mix and bake'
    }

    response = client.post('/recipes/create', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Cake" in response.data

def test_create_ingredient_post(client):
    form_data = {'name': 'Sugar', 'measures': 'cup'}
    response = client.post('/ingredient', data=form_data, follow_redirects=True)
    assert response.status_code == 200

def test_add_comment_post(client):
    with client.application.app_context():
        recipe = Recipe(title="Soup", instructions="Boil water", cuisine="other", cook_time=5, difficulty="easy")
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id

    form_data = {'author': 'TestUser', 'commentPost': 'Nice recipe'}
    response = client.post(f'/recipes/{recipe_id}', data=form_data)
    assert response.status_code == 200
    assert b"TestUser" in response.data

def test_delete_recipe_post(client):
    with client.application.app_context():
        recipe = Recipe(title="To Delete", instructions="Nothing", cuisine="other", cook_time=1, difficulty="easy")
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id

    response = client.post(f'/recipes/delete/{recipe_id}', follow_redirects=True)
    assert response.status_code == 200

def test_delete_comment_post(client):
    with client.application.app_context():
        recipe = Recipe(title="With Comment", instructions="Step", cuisine="other", cook_time=1, difficulty="easy")
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id

        comment = Comments(author="User", commentPost="Hi", recipe_id=recipe_id)
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

    response = client.post(f'/comments/delete/{comment_id}/{recipe_id}', follow_redirects=True)
    assert response.status_code == 200
