# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from app import app

# def test_create_recipe_valid_data():
#     with app.test_client() as c:
#         res = c.post('/create-recipe', data={
#             'title': 'Pancakes',
#             'instructions': 'Mix ingredients and cook.',
#             'cuisine': 'American',
#             'cook_time': 10,
#             'difficulty': 'Easy',
#             'ingredients': 'Flour, Eggs, Milk',
#         })
        
#         assert res.status_code == 200
#         assert b'Recipe saved successfully' in res.data

# def test_create_recipe_missing_title():
#     with app.test_client() as c:
#         res = c.post('/create-recipe', data={
#             'title': '',
#             'instructions': 'Mix ingredients and cook.',
#             'cuisine': 'American',
#             'cook_time': 10,
#             'difficulty': 'Easy',
#             'ingredients': 'Flour, Eggs, Milk',
#         })
        
#         assert res.status_code == 400
#         assert b'Title is required' in res.data

# def test_create_recipe_missing_cook_time():
#     with app.test_client() as c:
#         res = c.post('/create-recipe', data={
#             'title': 'Pancakes',
#             'instructions': 'Mix ingredients and cook.',
#             'cuisine': 'American',
#             'cook_time': '',
#             'difficulty': 'Easy',
#             'ingredients': 'Flour, Eggs, Milk',
#         })
        
#         assert res.status_code == 400
#         assert b'Cook time is required' in res.data

# def test_create_recipe_invalid_cook_time():
#     with app.test_client() as c:
#         res = c.post('/create-recipe', data={
#             'title': 'Pancakes',
#             'instructions': 'Mix ingredients and cook.',
#             'cuisine': 'American',
#             'cook_time': -5,
#             'difficulty': 'Easy',
#             'ingredients': 'Flour, Eggs, Milk',
#         })
        
#         assert res.status_code == 400
#         assert b'Cook time must be a positive number' in res.data

# def test_create_recipe_invalid_difficulty():
#     with app.test_client() as c:
#         res = c.post('/create-recipe', data={
#             'title': 'Pancakes',
#             'instructions': 'Mix ingredients and cook.',
#             'cuisine': 'American',
#             'cook_time': 10,
#             'difficulty': 'Very Hard',
#             'ingredients': 'Flour, Eggs, Milk',
#         })
        
#         assert res.status_code == 400
#         assert b'Invalid difficulty level' in res.data

# def test_create_recipe_invalid_cook_time_format():
#     with app.test_client() as c:
#         res = c.post('/create-recipe', data={
#             'title': 'Pancakes',
#             'instructions': 'Mix ingredients and cook.',
#             'cuisine': 'American',
#             'cook_time': 'ten',
#             'difficulty': 'Easy',
#             'ingredients': 'Flour, Eggs, Milk',
#         })
        
#         assert res.status_code == 400
#         assert b'Cook time must be a valid number' in res.data
