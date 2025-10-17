"""Launcher for Direct Preference Optimization training."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class DPOConfig:
    pairs: str
    init: str
    output: str
    beta: float
    epochs: int


def submit_dpo_job(config: DPOConfig) -> None:
    print("Submitting DPO job with config:")
    print(config)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch DPO training")
    parser.add_argument("--pairs", required=True)
    parser.add_argument("--init", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--beta", type=float, default=0.2)
    parser.add_argument("--epochs", type=int, default=2)
    args = parser.parse_args()

    config = DPOConfig(
        pairs=args.pairs,
        init=args.init,
        output=args.output,
        beta=args.beta,
        epochs=args.epochs,
    )
    submit_dpo_job(config)


if __name__ == "__main__":
    main()
