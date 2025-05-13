# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from app import app

# def test_search_by_title():
#     with app.test_client() as c:
#         # Search for 'Pancakes', which exists in the database
#         res = c.get('/recipes?query=Pancakes&filterType=title')
#         assert res.status_code == 200
#         assert b'Pancakes' in res.data

#         # Search for a recipe that doesn't exist (e.g., 'Pizza')
#         res = c.get('/recipes?query=Pizza&filterType=title')
#         assert res.status_code == 200
#         assert b'Pizza' not in res.data

#         # test results if empty query
#         res = c.get('/recipes?query=')
#         assert res.status_code == 200
#         assert b'Pancakes' in res.data

#         # check case insensitivity
#         res = c.get('/recipes?query=pancakes&filterType=title')
#         assert res.status_code == 200
#         assert b'Pancakes' in res.data

#         # check partial matches in title
#         res = c.get('/recipes?query=Pan&filterType=title')
#         assert res.status_code == 200
#         assert b'Pancakes' in res.data


# def test_search_by_cuisine():
#     with app.test_client() as c:
#         res = c.get('/recipes?query=&filterType=cuisineTypes&cuisineTypes=italian')
#         assert res.status_code == 200
#         assert b'Spaghetti Bolognese' in res.data

#         # search for recipe that does exist
#         res = c.get('/recipes?query=Tacos&filterType=cuisineTypes&cuisineTypes=mexican')
#         assert res.status_code == 200
#         assert b'Tacos' in res.data

#         # Search for a cuisine that doesn't exist
#         res = c.get('/recipes?query=Crepes&filterType=cuisineTypes&cuisineTypes=french')
#         assert res.status_code == 200
#         assert b'Crepes' not in res.data


# def test_search_by_difficulty():
#     with app.test_client() as c:
#         res = c.get('/recipes?query=&filterType=diff&diff=easy')
#         assert res.status_code == 200
#         assert b'Pancakes' in res.data
#         assert b'Greek Salad' in res.data

#         # check medium difficulty recipes
#         res = c.get('/recipes?query=&filterType=diff&diff=medium')
#         assert res.status_code == 200
#         assert b'Spaghetti Bolognese' in res.data
#         assert b'Tacos' in res.data


#         # check hard difficulty recipes
#         res = c.get('/recipes?query=&filterType=diff&diff=hard')
#         assert res.status_code == 200
#         assert b'Chicken Curry' in res.data
#         assert b'Sushi Rolls' in res.data


# def test_search_by_cook_time():
#     with app.test_client() as c:
#         # Valid filter: cook_time <= 20
#         res = c.get('/recipes?query=&filterType=time&time=20')
#         assert res.status_code == 200
#         assert b'Greek Salad' in res.data
#         assert b'Pancakes' in res.data
#         assert b'Spaghetti Bolognese' not in res.data

#         # Edge case: cook_time = 0 (should return nothing)
#         res = c.get('/recipes?query=&filterType=time&time=0')
#         assert res.status_code == 200
#         assert b'Greek Salad' not in res.data
#         assert b'Pancakes' not in res.data

#         # Edge case: missing time parameter, returns all recipes
#         res = c.get('/recipes?query=&filterType=time')
#         assert res.status_code == 200
#         assert b'Pancakes' in res.data



