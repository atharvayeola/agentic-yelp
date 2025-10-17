"""Core infrastructure stack stubs."""

from __future__ import annotations

from aws_cdk import Stack
from constructs import Construct


class CoreStack(Stack):
    """Provision S3 buckets, DynamoDB tables, and shared IAM roles."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore[override]
        super().__init__(scope, construct_id, **kwargs)
        # TODO: Define S3 buckets, DynamoDB tables, and IAM roles here.
