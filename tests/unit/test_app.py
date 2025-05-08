import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app import app

def test_homepage_accessible():
    app.config['TESTING'] = True
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    assert b'Recipe' in res.data
