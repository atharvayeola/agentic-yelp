"""API infrastructure stack stub."""

from __future__ import annotations

from aws_cdk import Stack
from constructs import Construct

from .core_stack import CoreStack


class ApiStack(Stack):
    """Expose REST endpoints for the TableTalk API."""

    def __init__(self, scope: Construct, construct_id: str, *, core_stack: CoreStack, **kwargs) -> None:  # type: ignore[override]
        super().__init__(scope, construct_id, **kwargs)
        self.core_stack = core_stack
        # TODO: Define API Gateway + Lambda/ECS resources referencing core_stack outputs.
