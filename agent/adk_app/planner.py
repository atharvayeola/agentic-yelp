"""Planner scaffolding for the TableTalk Google ADK agent.

The implementation in this module mirrors the patterns recommended by the
Google Agent Developer Kit (ADK) documentation:

* The planner receives structured ``Observation`` objects instead of raw
  strings.
* Planning results are returned as ``PlanResult`` containers that include both
  assistant responses and tool invocations.
* A mutable ``ConversationState`` tracks preferences and chat history in a
  normalised format so that ADK runtimes can serialise/deserialize the state
  safely between turns.

This file intentionally stays dependency free—no ADK imports—so that other
agents (or automated coding assistants) can swap in the concrete SDK classes
when wiring the real runtime.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence


ObservationRole = Literal["user", "assistant", "tool", "system"]


@dataclass
class Observation:
    """Lightweight mirror of ``adk.types.Observation``.

    Parameters
    ----------
    role:
        The source of the observation (``"user"``, ``"assistant"``,
        ``"tool"`` or ``"system"``).
    content:
        The raw payload from the runtime. For tool results this can be a
        dictionary; for utterances it is normally a string.
    tool_name:
        Optionally record which tool generated the observation. ADK best
        practices recommend tagging tool traces so downstream evaluators can
        reconstruct execution flows.
    """

    role: ObservationRole
    content: Any
    tool_name: Optional[str] = None


@dataclass
class ToolCall:
    """Represents a single tool invocation request."""

    name: str
    arguments: Dict[str, Any]
    description: Optional[str] = None


@dataclass
class PlanResult:
    """Planner output in the shape recommended by the ADK docs."""

    response: Optional[str]
    tool_calls: List[ToolCall] = field(default_factory=list)
    should_end: bool = False

    def to_wire_format(self) -> Dict[str, Any]:
        """Return a serialisable dictionary for runtime transport."""

        return {
            "response": self.response,
            "tool_calls": [
                {"name": call.name, "arguments": call.arguments, "description": call.description}
                for call in self.tool_calls
            ],
            "should_end": self.should_end,
        }


@dataclass
class ConversationState:
    """Mutable state shared across planner invocations."""

    preferences: Dict[str, Any] = field(default_factory=dict)
    history: List[Observation] = field(default_factory=list)

    REQUIRED_KEYS: Sequence[str] = ("diet", "budget", "distance_km", "location")

    def ingest_observation(self, observation: Observation) -> None:
        """Persist the observation to the history and update preferences."""

        self.history.append(observation)

        if observation.role == "user" and isinstance(observation.content, str):
            # In the full implementation we would run an extraction model. The
            # scaffold keeps it simple by storing the latest utterance so the
            # agent runner can plug in an NLU step later.
            self.preferences.setdefault("last_user_message", observation.content)

        if observation.role == "tool" and observation.tool_name == "menus.lookup":
            # Demonstrate how tool results could refresh the state (best
            # practice: normalise lookups to avoid repeated calls).
            self.preferences.setdefault("menus_cache", []).append(observation.content)

    def missing_preferences(self) -> List[str]:
        """Return preference keys that still need to be clarified."""

        missing: List[str] = []
        for key in self.REQUIRED_KEYS:
            value = self.preferences.get(key)
            if value in (None, "", [], {}):
                missing.append(key)
        return missing

    def last_user_message(self) -> Optional[str]:
        """Fetch the most recent user utterance from the history."""

        for observation in reversed(self.history):
            if observation.role == "user" and isinstance(observation.content, str):
                return observation.content
        return None


class TableTalkPlanner:
    """Google ADK-style planner placeholder."""

    def __init__(self) -> None:
        self._critic_enabled = True

    def plan(self, observation: Observation, state: ConversationState) -> PlanResult:
        """Given the current observation and mutable state, decide the next step."""

        state.ingest_observation(observation)

        if observation.role != "user":
            # Non-user events (e.g. tool results) don't trigger a direct
            # assistant response in the scaffold. The runtime will call us
            # again with the subsequent user input.
            return PlanResult(response=None, tool_calls=[])

        missing = state.missing_preferences()
        if missing:
            question = self._build_clarifying_question(missing)
            return PlanResult(response=question, tool_calls=[])

        tool_calls = [
            ToolCall(
                name="places.search",
                arguments=self._build_places_args(state.preferences),
                description="Primary recall step for candidate restaurants",
            )
        ]
        prompt = "Let me search for a few great options and circle back with suggestions."
        return PlanResult(response=prompt, tool_calls=tool_calls)

    def critic_filter(
        self, suggestions: Iterable[Dict[str, Any]], preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Filter suggestions that violate price or dietary constraints."""

        max_price = preferences.get("budget")
        dietary = set(map(str.lower, preferences.get("diet", [])))

        filtered: List[Dict[str, Any]] = []
        for item in suggestions:
            price_ok = max_price is None or item.get("price", 0) <= max_price
            tags = set(map(str.lower, item.get("tags", [])))
            diet_ok = not dietary or dietary.issubset(tags)
            if price_ok and diet_ok:
                filtered.append(item)
        return filtered

    @staticmethod
    def _build_clarifying_question(missing: Sequence[str]) -> str:
        friendly = ", ".join(missing)
        return f"Could you clarify your {friendly}?"

    @staticmethod
    def _build_places_args(preferences: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "near": preferences.get("location"),
            "cuisines": preferences.get("cuisine", []),
            "dietary": preferences.get("diet", []),
            "max_price": preferences.get("budget"),
            "distance_km": preferences.get("distance_km"),
        }


def _demo(prompt: str) -> None:
    """Quick command-line demo for the planner."""

    planner = TableTalkPlanner()
    state = ConversationState()
    observation = Observation(role="user", content=prompt)
    result = planner.plan(observation, state)
    print("Planner output:")
    print(result.to_wire_format())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo the TableTalk planner scaffold.")
    parser.add_argument("--demo-prompt", required=True, help="User utterance to feed into the planner")
    args = parser.parse_args()
    _demo(args.demo_prompt)
