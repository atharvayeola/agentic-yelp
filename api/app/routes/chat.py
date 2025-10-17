"""Chat endpoint scaffolding."""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from ..schemas.chat import ChatRequest
from ..services.agent_runner import AgentRunner

router = APIRouter(prefix="/chat", tags=["chat"])


def get_agent_runner() -> AgentRunner:
    return AgentRunner()


@router.post("", response_class=StreamingResponse)
async def chat_endpoint(payload: ChatRequest, runner: AgentRunner = Depends(get_agent_runner)) -> StreamingResponse:
    """Stream assistant tokens and tool events back to the client."""

    async def event_stream() -> AsyncGenerator[bytes, None]:
        async for chunk in runner.stream_chat(payload):
            yield (chunk + "\n").encode("utf-8")
            await asyncio.sleep(0)

    return StreamingResponse(event_stream(), media_type="application/jsonl")
