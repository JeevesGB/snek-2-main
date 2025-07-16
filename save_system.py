import json
import os

SAVE_PATH = "save_data/savegame.json"

def save_game(state):
    os.makedirs("save_data", exist_ok=True)
    with open(SAVE_PATH, "w") as f:
        json.dump(state, f)

def load_game():
    if not os.path.exists(SAVE_PATH):
        return None
    with open(SAVE_PATH, "r") as f:
        return json.load(f)
