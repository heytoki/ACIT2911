import json

# Instructions in JSON format (using Recipes id to match)
try:
    with open('instructions.json', 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {'-1': []}

# sample instructions JSON would look like:
# {'recipes id': ['content of step 1', 'content of step 2', ..., 'content of step n']}
# the value of the key(recipes id) would be a list which is iterable and ordered