import datetime
from typing import Dict
import encryption 
import dbHandler 


DEFAULT_FILE_PATH = 'users.json'

# sors = https://codereview.stackexchange.com/questions/198040/user-login-database-intended-for-beginners
# maybe other sors = https://stackoverflow.com/questions/54267646/i-want-to-use-json-in-python-to-save-users-and-password/54268080

def prepare_new_user_data(username: str, password: str) -> Dict:
    """
    Return user data ready for storage.
    :param username: The username for this user.
    :param password: The password for this user, in clear text.
    :return: A Dict containing user data ready to store, including encrypted password.
    """
    new_user = {
        'username': username,
        'password': encrypt_password(password)
    }
    return new_user


def check_if_user_already_exists(username: str, json_file_path: str=DEFAULT_FILE_PATH) -> bool:
    """
    Queries a JSON file and returns whether it already exists.
    :param username: The username to check for duplication.
    :param json_file_path: The path where the JSON file is located.
    :return: Whether the username already exists.
    """
    all_users = get_json_file_contents(json_file_path)
    if not all_users:
        return False
    for user in all_users:
        if user['username'] == username:
            return True
    return False


def add_user(username: str, password: str, json_file_path: str=DEFAULT_FILE_PATH) -> None:
    """
    Adds a user to a JSON file, unless it is a duplicate, in which case it raises a ValueError.
    :param username: The username of the user to add.
    :param password: The password of the user to add, in clear text.
    :param json_file_path: The path where the JSON file to add the user to is located.
    :return: None
    """
    create_file_if_not_exists(json_file_path)
    is_duplicate_user = check_if_user_already_exists(username, json_file_path)
    if is_duplicate_user:
        raise ValueError(f'Username "{username}" already exists.')
    new_user = prepare_new_user_data(username, password)
    all_users = get_json_file_contents(json_file_path)
    if not all_users:
        all_users = []
    all_users.append(new_user)
    with open(json_file_path, 'w') as users_file:
        json.dump(all_users, users_file, indent=2)


def retrieve_user(username: str, json_filepath: str=DEFAULT_FILE_PATH) -> Union[Dict, None]:
    """
    Returns a single user record from the target JSON file.
    :param username: the username to search for.
    :param json_filepath: The path where the JSON file to retrieve the user from is located.
    :return: The user record as a Dict, or None if it is not found.
    """
    all_users = get_json_file_contents(json_filepath)
    for user in all_users:
        if user['username'] == username:
            return user
    return None


def authenticate_username_and_password(username: str, password: str) -> bool:
    """
    Verify that the provided username and password match what is stored in the user data,
    for authentication purposes.
    :param username: The user's username.
    :param password: The user's password, in clear text.
    :return: Whether the authentication was successful.
    """
    user = retrieve_user(username)
    password_hash = user['password']
    if not user:
        return False
    if not check_password(password, password_hash):
        return False
    return True


if __name__ == '__main__':
    test_username = 'test1'
    test_password = 'Password1'
    print(prepare_new_user_data(test_username, test_password))
    test_file_path = 'data/test_database.json'
    create_file_if_not_exists(test_file_path)
    add_user(test_username, test_password, test_file_path)
    print(get_json_file_contents(test_file_path))