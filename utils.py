# this is where put functions and stuff that we call in other files

import json

def save_instructions_to_json(recipe_id, instructions_text):
    instructions_file = "instructions.json"

    # this condition will support both list and string inputs
    if isinstance(instructions_text, list):
        steps = [line.strip() for line in instructions_text if line.strip()]
    elif isinstance(instructions_text, str):
        steps = [line.strip() for line in instructions_text.strip().split('\n') if line.strip()]
    else:
        steps = []

    # Load existing data or if no data found it will start fresh
    try:
        with open(instructions_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Store under the recipe ID
    data[str(recipe_id)] = steps

    # Save to file
    with open(instructions_file, 'w') as f:
        json.dump(data, f, indent=4)
