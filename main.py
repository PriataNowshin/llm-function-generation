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
from src.io_helper import load_data_from_jsonl, write_data_into_json
from src.llm_client import build_config, generate_requirement, regenerate_function


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

    return MODEL_MAP.get(llm, llm)


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

    output: List[Dict[str, Any]] = []
    for idx, record in enumerate(load_data_from_jsonl(input_path), start=1):
        print("====" * 20)
        old_code = record.get("full_old_function_code") or ""
        new_code = record.get("full_new_function_code") or ""

        print("Old code:", old_code)
        print("\n\n")
        print("New code:", new_code)

        requirement = generate_requirement(old_code, new_code, config)
        print("\n\n")
        new_function_code_by_llm = regenerate_function(old_code, requirement, config)

        output.append(
            {
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
        )

        print("====" * 20)

        # if idx % 10 == 0:
        print(f"Processed {idx} records...", file=sys.stderr)

        print("\n" * 5)

    write_data_into_json(output_path, output)
    print(f"Wrote {len(output)} records to {output_path}")


if __name__ == "__main__":
    main()
