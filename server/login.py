import datetime
import json

from server.encryption import hash_password, check_password
from server.dbHandler import get_json_file_contents, create_file_if_not_exists

jsonDb = "users.json"

# Source = https://codereview.stackexchange.com/questions/198040/user-login-database-intended-for-beginners
## maybe other sors = https://stackoverflow.com/questions/54267646/i-want-to-use-json-in-python-to-save-users-and-password/54268080


def prepare_user(username: str, password: str, name: str, email: str):
    new_user = {
        "Username": username,
        "Password": hash_password(password),
        "Name": name,
        "Email": email,
    }
    return new_user


def add_user(username: str, password: str, name: str, email: str):
    create_file_if_not_exists(jsonDb)
    is_duplicate_user = retrieve_user(username, jsonDb)
    if is_duplicate_user != False:
        raise ValueError(f'Username "{username}" already exists.')
    new_user = prepare_user(username, password, name, email)
    all_users = get_json_file_contents(jsonDb)
    if not all_users:
        all_users = []
    all_users.append(new_user)
    with open(jsonDb, "w") as users_file:
        json.dump(all_users, users_file, indent=2)


def retrieve_user(username: str):
    all_users = get_json_file_contents(jsonDb)
    for user in all_users:
        if user["username"] == username:
            return user
    return None


def auth_user(username: str, password: str):
    user = retrieve_user(username)
    password_hash = user["password"]
    if not user:
        return False
    if not check_password(password, password_hash):
        return False
    return True
