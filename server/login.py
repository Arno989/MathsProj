import datetime
import json

from encryption import hash_password, check_password
from dbHandler import get_json_file_contents, create_file_if_not_exists
from data.movie import User

jsonDb = "server/users.json"

# Source = https://codereview.stackexchange.com/questions/198040/user-login-database-intended-for-beginners
## maybe other sors = https://stackoverflow.com/questions/54267646/i-want-to-use-json-in-python-to-save-users-and-password/54268080


def add_user(username: str, password: str, name: str, email: str):
    create_file_if_not_exists(jsonDb)
    print("create db")
    is_duplicate_user = retrieve_user(username)
    print("aaa")
    print(f"check user dup {is_duplicate_user}")
    print("bbb")
    if is_duplicate_user != False:
        raise ValueError(f'Username "{username}" already exists., why am i called?')
    new_user = User(
        username=username, password=hash_password(password), name=name, email=email
    )
    print("created user")
    all_users = get_json_file_contents(jsonDb)
    print(f"all users = {all_users}")
    if not all_users:
        all_users = []
    all_users.append(new_user)
    with open(jsonDb, "w") as users_file:
        json.dump(all_users, users_file, indent=2)


def retrieve_user(username: str):
    all_users = get_json_file_contents(jsonDb)
    print(all_users)
    print(len(all_users))
    if len(all_users) != 0:
        for u in all_users:
            if u.get(username) == username:
                return True
        return False
    else:
        return False


def auth_user(username: str, password: str):
    user = retrieve_user(username)
    password_hash = user["password"]
    if not user:
        return False
    if not check_password(password, password_hash):
        return False
    return True
