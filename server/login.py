import datetime
import json
import os
import sys

from server.encryption import hash_password, check_password
from server.dbHandler import get_json_file_contents, create_file_if_not_exists
from data.movie import User

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)
jsonDb = f"{PROJECT_ROOT}\\data\\users.json"


def add_user(username: str, password: str, name: str, email: str):
    create_file_if_not_exists(jsonDb)
    is_duplicate_user = retrieve_user(username)
    if is_duplicate_user != None:
        print(f'Username "{username}" already exists.')
    new_user = User(
        username=username, password=hash_password(password), name=name, email=email
    )
    all_users = get_json_file_contents(jsonDb)
    all_users.append(new_user.__dict__)
    with open(jsonDb, "w") as users_file:
        json.dump(all_users, users_file, indent=4)


def retrieve_user(username: str):
    all_users = get_json_file_contents(jsonDb)
    if len(all_users) != 0:
        for u in all_users:
            if u['username'] == username:
                return u
        return None
    else:
        return None


def auth_user(username: str, password: str):
    user = retrieve_user(username)
    password_hash = user['password']
    if not user:
        return False
    if not check_password(password, password_hash):
        return False
    return True
