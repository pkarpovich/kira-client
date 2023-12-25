import json
from typing import Any


class BaseFileStore:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> Any:
        with open(self.file_path, "r") as file:
            return json.load(file)
