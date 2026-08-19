import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "data"


def read_json(filename: str) -> list:
    file_path = BASE_DIR / filename

    with open(file_path, "r") as file:
        return json.load(file)


def write_json(filename: str, data):
    file_path = BASE_DIR / filename

    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
