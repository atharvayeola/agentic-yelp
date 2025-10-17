"""Kick off a Bedrock or SageMaker SFT job."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class TrainConfig:
    s3_input: str
    output: str
    base_model: str
    epochs: int
    lr: float


def submit_job(config: TrainConfig) -> None:
    """Placeholder: invoke Bedrock or SageMaker training APIs."""

    print("Submitting SFT job with config:")
    print(config)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch SFT training")
    parser.add_argument("--s3-input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=1e-4)
    args = parser.parse_args()

    config = TrainConfig(
        s3_input=args.s3_input,
        output=args.output,
        base_model=args.base_model,
        epochs=args.epochs,
        lr=args.lr,
    )
    submit_job(config)


if __name__ == "__main__":
    main()
