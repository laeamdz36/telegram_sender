"""Test json loader from json file"""
import json
from pathlib import Path


def load_json(file_name):
    """Load json form local path"""

    path_file = Path(__file__).parent.resolve().joinpath(file_name)
    json_data = None
    try:
        with open(path_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        json_data = data
    except FileNotFoundError:
        print(f"File not found {path_file}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode json file: {e}")

    return json_data


def get_db_metadata(json_data):
    """Analyze the json data and get all metadata"""

    if json_data is not None:
        print(json_data["databases"])
        for db in json_data["databases"]:
            print(f"Name: {db['name']} EXT: {db['extension']}")


def build_path():
    """Build the ptah"""
    target_path = None
    path = Path(__file__).resolve()
    for p in path.parents:
        if "telegram_reporter" in str(p.name):
            target_path = p
            break
    print(f"TARGET: {target_path}")


if __name__ == "__main__":
    build_path()
