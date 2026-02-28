import json
import os

def load_rubric():
    """
    Loads the Week 2 rubric JSON for use in system prompts and judge logic.
    """
    rubric_path = os.path.join(os.path.dirname(__file__), '../../rubric/week2_rubric.json')
    with open(rubric_path, 'r') as f:
        return json.load(f)

RUBRIC = load_rubric()
