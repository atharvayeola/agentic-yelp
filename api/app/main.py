"""FastAPI entrypoint for the TableTalk backend."""

from __future__ import annotations

from fastapi import FastAPI

from .routes import chat

app = FastAPI(title="TableTalk API", version="0.1.0")
app.include_router(chat.router)


@app.get("/healthz", tags=["health"])
async def healthcheck() -> dict[str, str]:
    """Simple health endpoint for monitoring."""

    return {"status": "ok"}
