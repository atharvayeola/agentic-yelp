"""Frontend hosting stack stub."""

from __future__ import annotations

from aws_cdk import Stack
from constructs import Construct

from .api_stack import ApiStack


class FrontendStack(Stack):
    """Serve the Next.js app via S3/CloudFront."""

    def __init__(self, scope: Construct, construct_id: str, *, api_stack: ApiStack, **kwargs) -> None:  # type: ignore[override]
        super().__init__(scope, construct_id, **kwargs)
        self.api_stack = api_stack
        # TODO: Define S3 bucket, CloudFront distribution, and outputs.
