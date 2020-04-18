import json
from pathlib import Path
from typing import List, Union
from data.movie import User

startUsers = []
startUsers.append(User(username="test", password="test"))
startUsers.append(User(username="test2", password="test2"))

def obj_dict(obj):
    return obj.__dict__

def create_file_if_not_exists(path: str):
    if not Path(path).is_file():
        with open(path, "w") as users_file:
            json.dumps(startUsers, users_file, indent=4, default=obj_dict)


def get_json_file_contents(path: str):
    with open(path) as users_file:
        content = json.loads(users_file, object_hook=User)
        print(content)
        return content
