import json
import os

DEFAULT_SETTINGS = {
    "window_size": [1280, 960],
    "volume": 0.5,
    "difficulty": "normal"
}

SETTINGS_FILE = "config/settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    os.makedirs("config", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
