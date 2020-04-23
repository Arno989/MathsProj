import json
from pathlib import Path
from data.movie import User

startUsers = [
    User(name="yeet", username="yeet", password="hash", email="yeet"),
    User(name="yeet2", username="yeet2", password="hash2", email="yeet2"),
]


def obj_dict(obj):
    return obj.__dict__


def create_file_if_not_exists(path: str):
    if not Path(path).is_file():
        with open(path, "w") as users_file:
            json.dump([ob.__dict__ for ob in startUsers], users_file)


def get_json_file_contents(path: str):
    with open(path) as users_file:
        return json.load(users_file)
