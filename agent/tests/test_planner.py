"""Unit tests for the TableTalk planner skeleton."""

from agent.adk_app.planner import ConversationState, Observation, PlanResult, TableTalkPlanner


def test_plan_requests_clarification_when_preferences_missing() -> None:
    planner = TableTalkPlanner()
    state = ConversationState()

    observation = Observation(role="user", content="I want vegan ramen")
    result = planner.plan(observation, state)

    assert isinstance(result, PlanResult)
    assert result.response is not None and "clarify" in result.response.lower()
    assert result.tool_calls == []


def test_plan_enqueues_places_search_when_preferences_present() -> None:
    planner = TableTalkPlanner()
    state = ConversationState(
        preferences={
            "diet": ["vegan"],
            "budget": 25,
            "distance_km": 5,
            "location": "94105",
        }
    )

    observation = Observation(role="user", content="Thanks")
    result = planner.plan(observation, state)

    assert result.tool_calls, "Expected tool queue with places.search call"
    assert result.tool_calls[0].name == "places.search"
