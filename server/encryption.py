import bcrypt  # u gotta "pip install bcrypt" bro // done


def hash_password(password: str) -> str:
    encoded_password = password.encode("utf8")
    cost_rounds = 12 # tegen de bruteforce jwz
    random_salt = bcrypt.gensalt(cost_rounds)
    hashed_password = bcrypt.hashpw(encoded_password, random_salt).decode(
        "utf8", "strict"
    )
    return hashed_password


def check_password(password: str, password_hash: str) -> bool:
    encoded_password = password.encode("utf8")
    encoded_password_hash = password_hash.encode("utf8")
    password_matches = bcrypt.checkpw(encoded_password, encoded_password_hash)
    return password_matches
