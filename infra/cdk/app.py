"""AWS CDK application entrypoint."""

from __future__ import annotations

import aws_cdk as cdk

from stacks.core_stack import CoreStack
from stacks.api_stack import ApiStack
from stacks.frontend_stack import FrontendStack


app = cdk.App()
core = CoreStack(app, "TableTalkCore")
api = ApiStack(app, "TableTalkApi", core_stack=core)
FrontendStack(app, "TableTalkFrontend", api_stack=api)

app.synth()
