import json
import os


def dump_json(data: dict, name: str, path: str = "data/") -> bool:
    """
    Dumps a dictionary to a JSON file.

    Args:
        data (dict): The dictionary to dump.
        name (str): The name of the JSON file (without extension).
        path (str, optional): The directory to save the JSON file. Defaults to "data/".
    """
    try:
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f"{name}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        return True
    except Exception as e:
        return False


def load_json(name: str, path: str = "data/") -> dict:
    """
    Loads a dictionary from a JSON file.

    Args:
        name (str): The name of the JSON file (without extension).
        path (str, optional): The directory where the JSON file is located. Defaults to "data/".

    Returns:
        dict: The loaded dictionary.
    """
    try:
        file_path = os.path.join(path, f"{name}.json")
        with open(file_path, "r") as f:
            data = json.load(f)

        return data
    except Exception as e:
        return {}


def load_json_file(file_path: str) -> dict:
    """
    Loads a dictionary from a JSON file using the full file path.

    Args:
        file_path (str): The full path to the JSON file (including extension).

    Returns:
        dict: The loaded dictionary, or empty dict if file not found or error.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}
    except Exception as e:
        return {}

