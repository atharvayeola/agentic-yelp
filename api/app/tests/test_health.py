"""Smoke test for FastAPI health endpoint."""

import pytest

fastapi = pytest.importorskip("fastapi")  # type: ignore
TestClient = pytest.importorskip("fastapi.testclient").TestClient  # type: ignore

from api.app.main import app


def test_healthcheck() -> None:
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
