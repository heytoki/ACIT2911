# manage.py
# File to store functions that we can call in other files

import json

def save_instructions_to_json(recipe_id, instructions_text):
    instructions_file = "instructions.json"
    steps = [line.strip() for line in instructions_text.strip().split('\n') if line.strip()]

    try:
        with open(instructions_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[str(recipe_id)] = steps

    with open(instructions_file, 'w') as f:
        json.dump(data, f, indent=4)
