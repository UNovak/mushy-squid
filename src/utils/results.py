import csv
import json
import uuid
from pathlib import Path
from random import randint
from typing import Any


def resolve_seed(seed: int | None) -> int:
    """Return the provided seed, or generate one if missing."""
    return seed if seed is not None else randint(0, 2_147_483_647)


def generate_run_id() -> str:
    """Return a unique run identifier."""
    return str(uuid.uuid4())


def write_algorithm_results(
    output_file: str,
    dataset: str,
    seed: int,
    run_id: str,
    solutions: list[tuple[int, list[int], float, int]],
    metadata: dict[str, Any],
) -> None:
    """
    Append incumbent improvements to a CSV file.

    Expected solutions tuple format:
    (cost, seq, elapsed_time, iteration)
    """
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "dataset",
        "run_id",
        "seed",
        "algorithm_type",
        "iteration_limit",
        "total_time",
        "cost",
        "solution",
        "elapsed_time",
        "iteration",
    ]

    file_exists = path.exists() and path.stat().st_size > 0

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for cost, seq, elapsed_time, iteration in solutions:
            writer.writerow({
                "dataset": dataset,
                "run_id": run_id,
                "seed": seed,
                "algorithm_type": metadata.get("algorithm_type"),
                "iteration_limit": metadata.get("iteration_limit"),
                "total_time": round(float(metadata.get("total_time", 0.0)), 6),
                "cost": int(cost),
                "solution": json.dumps(seq),
                "elapsed_time": round(float(elapsed_time), 6),
                "iteration": int(iteration),
            })
