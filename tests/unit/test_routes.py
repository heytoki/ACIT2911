import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.test_client() as client:
        with app.app_context():
            from db import db
            db.create_all()
        yield client

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_page_loads(client):
    response = client.get('/recipes/create')
    assert response.status_code == 200

def test_ingredient_page_loads(client):
    response = client.get('/ingredient')
    assert response.status_code == 200

def test_recipes_page_loads(client):
    response = client.get('/recipes?query=&filterType=title')
    assert response.status_code == 200

