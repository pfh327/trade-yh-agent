from __future__ import annotations

import json
from pathlib import Path
from time import time


def append_case_log(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"created_at": time(), **payload}
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

