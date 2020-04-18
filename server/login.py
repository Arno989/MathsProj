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
    print(f"check user dup")
    is_duplicate_user = retrieve_user(username)
    print(f"user dup {is_duplicate_user}")
    if is_duplicate_user != False:
        print(f'Username "{username}" already exists. server side')
    new_user = User(username=username, password=hash_password(password), name=name, email=email)
    print(f"created user : {new_user}")
    all_users = get_json_file_contents(jsonDb)
    print(f"all users = {all_users}")
    print(f"filetype {type(all_users)}")
    print(f"filetype {type(all_users[0])}")
    print(new_user.__dict__)
    all_users.append(new_user.__dict__)
    print("appendededed")
    with open(jsonDb, "w") as users_file:
        print(f"dumping {all_users}")
        json.dump(all_users, users_file, indent=4)


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
