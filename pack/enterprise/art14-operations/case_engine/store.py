"""JSON-file case store (one file holding all cases). Writes are atomic."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {"cases": {}}
        return json.loads(self.path.read_text())

    def save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w") as fh:
            json.dump(data, fh, indent=2, sort_keys=False)
        os.replace(tmp, self.path)

    def get(self, case_id: str) -> dict:
        data = self.load()
        if case_id not in data["cases"]:
            raise KeyError(f"no case {case_id}")
        return data["cases"][case_id]

    def put(self, case: dict) -> None:
        data = self.load()
        data["cases"][case["id"]] = case
        self.save(data)

    def all(self) -> list[dict]:
        return list(self.load()["cases"].values())
