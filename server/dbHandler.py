import json
from pathlib import Path
from typing import List, Union


def create_file_if_not_exists(path: str) -> None:
    Path(path).touch()


def get_json_file_contents(path: str) -> Union[List, None]:
    try:
        json_file = open(path)
    except IOError:
        return None
    try:
        content = json.load(json_file)
    except ValueError:
        content = None
    json_file.close()
    return content
