"""Bridge between FastAPI and the ADK planner."""

from __future__ import annotations

import json
from typing import AsyncGenerator

from agent.adk_app.planner import ConversationState, TableTalkPlanner
from agent.tools import BookingTools, MenuLookupTool, PlacesSearchTool
from ..schemas.chat import ChatRequest


class AgentRunner:
    """Executes the planner loop and yields streaming chunks."""

    def __init__(self) -> None:
        self._planner = TableTalkPlanner()
        self._places = PlacesSearchTool()
        self._menus = MenuLookupTool()
        self._booking = BookingTools()
        self._sessions: dict[str, ConversationState] = {}

    async def stream_chat(self, payload: ChatRequest) -> AsyncGenerator[str, None]:
        state = self._sessions.setdefault(
            payload.session_id,
            ConversationState(preferences={}, history=[]),
        )
        result = self._planner.plan(state, payload.message)

        yield json.dumps({"type": "plan", "data": result})

        for tool in result["tool_queue"]:
            name = tool["name"]
            args = tool["arguments"]
            if name == "places.search":
                data = self._places.search(**args)
            elif name == "menus.lookup":
                data = self._menus.lookup(**args)
            elif name == "book.deeplink":
                data = self._booking.make_deeplink(**args)
            else:
                data = {"error": f"unknown tool {name}"}
            yield json.dumps({"type": "tool_result", "name": name, "data": data})

        yield json.dumps({"type": "final", "data": "TODO: integrate Bedrock completion"})
