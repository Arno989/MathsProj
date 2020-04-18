import json
from pathlib import Path
from typing import List, Union
from data.movie import User

startUsers = '{"username": "jan", "password": "dfgf","name": "janneke", "email":"jan@hotmail.com"}'


def obj_dict(obj):
    return obj.__dict__

def create_file_if_not_exists(path: str):
    if not Path(path).is_file():
        with open(path, "w") as users_file:
            json.dumps(startUsers, users_file)
            #dumps


def get_json_file_contents(path: str):
    with open(path) as users_file:
        #loads
        content = json.load(users_file)
        #content = json.load(users_file, object_hook=User)
        print(content)
        return content
