import pytest
from app import create_app
from db import db
from models import Recipe

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            r1 = Recipe(title="Spaghetti Bolognese", instructions="Boil pasta", cuisine="italian", cook_time=30, difficulty="medium")
            r2 = Recipe(title="Sushi Rolls", instructions="Roll rice", cuisine="japanese", cook_time=50, difficulty="hard")
            db.session.add_all([r1, r2])
            db.session.commit()
        yield client

def test_search_by_title(client):
    response = client.get('/recipes?query=Spaghetti&filterType=title')
    assert response.status_code == 200
    assert b"Spaghetti Bolognese" in response.data
    assert b"Sushi Rolls" not in response.data

def test_search_by_cuisine(client):
    response = client.get('/recipes?query=Sushi&filterType=cuisineTypes&cuisineTypes=japanese')
    assert response.status_code == 200
    assert b"Sushi Rolls" in response.data
    assert b"Spaghetti Bolognese" not in response.data

def test_search_by_difficulty(client):
    response = client.get('/recipes?query=Sushi&filterType=diff&diff=hard')
    assert response.status_code == 200
    assert b"Sushi Rolls" in response.data
    assert b"Spaghetti Bolognese" not in response.data

def test_search_by_cook_time(client):
    response = client.get('/recipes?query=Sushi&filterType=time&time=60')
    assert response.status_code == 200
    assert b"Sushi Rolls" in response.data

def test_search_empty_query(client):
    response = client.get('/recipes?query=&filterType=title')
    assert response.status_code == 200
    assert b"Spaghetti Bolognese" in response.data
    assert b"Sushi Rolls" in response.data

def test_search_time_non_numeric(client):
    response = client.get('/recipes?query=Sushi&filterType=time&time=abc')
    assert response.status_code == 500 or response.status_code == 200
