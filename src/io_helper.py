"""I/O helpers for loading JSONL inputs and writing JSON outputs."""

import json
import os
from typing import Any, Dict, Iterable, List


def load_data_from_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    """Load JSON objects from a JSONL file.

    Reads the file line-by-line and yields one parsed JSON object per non-empty
    line.

    Args:
        path: Path to the input JSONL file.

    Returns:
        An iterator that yields dictionaries parsed from each JSON line.
    """
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_data_into_json(path: str, payload: List[Dict[str, Any]]) -> None:
    """Write a list of JSON-serializable objects to a JSON file.

    Creates the parent directory for the output file if it does not already
    exist.

    Args:
        path: Output file path.
        payload: List of dictionaries to write as a JSON array.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=True, indent=2)
