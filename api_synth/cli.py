from __future__ import annotations

import argparse
import json

from .generator import TaskGenerator, summarize
from .validator import validate_batch


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate API-spec implementation tasks")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--min-nonstandard-ratio", type=float, default=0.3)
    parser.add_argument("--output", default="tasks.json")
    args = parser.parse_args()

    generator = TaskGenerator(seed=args.seed)
    tasks = generator.generate_batch(args.count, min_nonstandard_ratio=args.min_nonstandard_ratio)
    validate_batch(tasks, min_nonstandard_ratio=args.min_nonstandard_ratio)

    payload = {
        "tasks": [t.to_dict() for t in tasks],
        "summary": summarize(tasks).to_dict(),
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
