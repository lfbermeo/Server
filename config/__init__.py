import json as __json
from os import path as __path
from sys import argv as __argv
from typing import cast as __cast


def __get_config(key: str, default: str) -> str:
    with open('config-server.json', encoding='utf8') as file:
        json_obj = __json.load(file)
        return __cast(str, json_obj[key]) if key in json_obj else default


PORT: int = int(__argv[1]) if len(__argv) > 1 else 8000
TEMP_FILES_DIR: str = __path.join(__get_config('tempFolder', 'temp'))
INPUT_FOLDER: str = __path.join(TEMP_FILES_DIR, __get_config('inputFolder', 'input'))
OUTPUT_FOLDER: str = __path.join(TEMP_FILES_DIR, __get_config('outputFolder', 'output'))

__all__ = ["INPUT_FOLDER", "PORT", "OUTPUT_FOLDER", "TEMP_FILES_DIR"]
