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


def load_processed_function_names(path: str) -> set:
    """Load the set of processed function names from an existing output JSON file.

    This is used to avoid re-processing functions when appending to an existing
    output file.

    Args:
        path: Path to the existing output JSON file.

    Returns:
        A set of function names that have already been processed.
    """
    function_names = set()

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for record in data:
                function_names.add(record.get("function_name"))

    return function_names


def append_record_to_json(path: str, record: Dict[str, Any]) -> None:
    """Append or update a single record in the JSON array file.
    
    If the file doesn't exist, creates it with the record as the first element.
    If the file exists, loads the current array, appends the new record, and 
    writes back.
    
    Args:
        path: Path to the output JSON file.
        record: Dictionary to append.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    data = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

    data.append(record)
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=True, indent=2)
