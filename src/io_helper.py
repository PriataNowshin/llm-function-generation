"""I/O helpers for loading JSONL inputs and writing JSON outputs."""

import json
import os
from typing import Any, Dict, List


def load_data_from_jsonl(path: str) -> List[Dict[str, Any]]:
    """Load JSON objects from a JSONL file.

    Reads the file line-by-line and returns one parsed JSON object per non-empty
    line.

    Args:
        path: Path to the input JSONL file.

    Returns:
        A list of dictionaries parsed from each JSON line.
    """
    records: List[Dict[str, Any]] = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    return records


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
