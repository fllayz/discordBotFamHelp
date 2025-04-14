import json
import logging
from pathlib import Path
from contextlib import contextmanager

class Database:
    def __init__(self, name: str):
        self.path = Path(f"database/{name}.json")
        self.path.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger("Database")

    @contextmanager
    def transaction(self):
        data = self._read()
        try:
            yield data
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise
        finally:
            self._write(data)

    def _read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)