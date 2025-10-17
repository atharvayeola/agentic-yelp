"""Data preprocessing utilities for SFT."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def iter_examples(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def main(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    with output.open("w", encoding="utf-8") as sink:
        for example in iter_examples(source):
            key = example["messages"][1]["content"]
            if key in seen:
                continue
            seen.add(key)
            sink.write(json.dumps(example) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prep SFT dataset")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    main(args.source, args.output)
