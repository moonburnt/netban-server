from dotenv import load_dotenv, find_dotenv
from os import environ
from pathlib import Path
from typing import Any


class NotSet:
    pass


class EnvLoader:
    """Dotenv loader with optional typing support."""

    def __init__(self, path: str | Path | None = None):
        self.path = path or find_dotenv()

    def load(self):
        load_dotenv(self.path)

    def get_var(self, key: str, default: Any | NotSet = NotSet) -> Any:
        if isinstance(default, NotSet):
            return environ[key]
        else:
            return environ.get(key, default=default)

    def get_str(self, key: str, default: str | NotSet = NotSet) -> str:
        return str(self.get_var(key, default))

    def get_int(self, key: str, default: int | NotSet = NotSet) -> int:
        return int(self.get_var(key, default))

    def get_float(self, key: str, default: float | NotSet = NotSet) -> float:
        return float(self.get_var(key, default))

    def get_bool(self, key: str, default: bool | NotSet = NotSet) -> bool:
        # Opinionated, may aswell support 'true'/'false' style
        return bool(self.get_int(key, default))

    def get_list(self, key: str) -> list[str]:
        return [i.strip() for i in self.get_var(key, "").split(",")]
