# Selection of useful functions

from typing import Any


def write_to_json(data: Any, json_file: str) -> None:
    """Write Data to JSON File

    The content of the JSON is completely deleted and replaced by the new content written into the file

    Args:
        data: preferably structured data such as lists or dictionaries to be stored in a JSON file
    """
    import json

    with open(json_file, "w") as file:
        contents = json.dumps(data, indent=2)
        file.write(contents)


def read_from_json(json_file: str) -> Any:
    """Import data from JSON file

    The content of the JSON file is completely copied and converted into a python data structure,
    which is returned by the function.

    Args:
        json_file (name.json): Name of a json file stored in working directory

    Returns:
        _type_: content of the JSON file as list or dictionary
    """
    import json

    with open(json_file, "r") as file:
        contents = file.read()
        data = json.loads(contents)
    return data


if __name__ == "__main__":
    pass
