"""Offline evaluation harness stub."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def load_cases(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        import yaml  # type: ignore

        return yaml.safe_load(handle)


def main() -> None:
    cases = load_cases(Path(__file__).with_name("test_cases.yaml"))
    print(json.dumps({"cases": len(cases)}))


if __name__ == "__main__":
    main()
