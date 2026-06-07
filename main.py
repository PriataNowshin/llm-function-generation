#!/usr/bin/env python3
"""Entry point for LLM function-generation dataset creation."""

import argparse
import os
import sys
from typing import Any, Dict, List

from src.constants import (
    DATA_DIR,
    INPUT_FILENAME,
    OUTPUT_FILENAME,
    MODEL_MAP,
    OUTPUT_DIR,
)
from src.io_helper import (
     load_data_from_jsonl,
     load_processed_function_names,
     append_record_to_json,
)
from src.llm_client import (
    build_config, 
    generate_requirement, 
    generate_function
)


def resolve_llm_model_from_arg(llm: str) -> str:
    """Resolve a CLI model alias to a concrete model identifier.

    The provided value is stripped. If it matches a key in MODEL_MAP, the mapped
    model identifier is returned; otherwise the stripped value itself is
    returned.

    Args:
        llm: Model alias or model identifier provided via the command line.

    Returns:
        The resolved model identifier to send to the LLM provider.

    Raises:
        SystemExit: If llm is empty after stripping.
    """
    llm = llm.strip()
    if not llm:
        raise SystemExit("Model alias must be a non-empty string.")

    if llm not in MODEL_MAP:
        known = ", ".join(sorted(MODEL_MAP))
        raise KeyError(f"Unknown model alias {llm!r}. Choose one of: {known}")

    return MODEL_MAP[llm]


def main() -> None:
    """Run the dataset generation pipeline.

    Parses command-line arguments, loads records from the input JSONL file,
    calls the LLM to generate a requirement and regenerated function code for
    each record, and writes the resulting dataset to a JSON file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", help="Model alias to use.", required=True)

    args = parser.parse_args()

    llm = resolve_llm_model_from_arg(args.llm)

    input_path = os.path.join(DATA_DIR, INPUT_FILENAME)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    config = build_config(llm)

    processed_function_names = load_processed_function_names(output_path)

    for idx, record in enumerate(load_data_from_jsonl(input_path), start=1):

        if record.get("function_name") in processed_function_names:
            print(f"Skipping already processed function {record.get('function_name')}", file=sys.stderr)
            continue

        old_code = record.get("full_old_function_code")
        new_code = record.get("full_new_function_code")

        requirement = generate_requirement(old_code, new_code, config)
        new_function_code_by_llm = generate_function(old_code, requirement, config)

        output_record = {
                "repo_full_name": record.get("repo_full_name"),
                "file_path": record.get("file_path"),
                "function_name": record.get("function_name"),
                "old_commit_sha": record.get("old_commit_sha"),
                "new_commit_sha": record.get("new_commit_sha"),
                "old_commit_message": record.get("old_commit_message"),
                "new_commit_message": record.get("new_commit_message"),
                "old_function_code": record.get("full_old_function_code"),
                "new_function_code": record.get("full_new_function_code"),
                "requirement": requirement,
                "new_function_code_by_llm": new_function_code_by_llm,
            }

        append_record_to_json(output_path, output_record)

        if idx % 10 == 0:
            print(f"Processed {idx} records...", file=sys.stderr)

    print(f"Completed processing records to {output_path}")


if __name__ == "__main__":
    main()
