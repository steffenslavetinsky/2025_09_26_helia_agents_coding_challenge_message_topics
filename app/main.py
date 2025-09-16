from fastapi import FastAPI
from app.models import HealthCheckResponse, HealthStatus
from typing import Annotated
from pydantic import Field

app = FastAPI()


@app.get(
    "/analytics/hot-topics",
    summary="Get hot topics from messages",
    description="Analyze conversations/messages and return the n hottest topics along with related conversations.",
)
def analyze_message_hot_topics(
    number_of_topics: Annotated[
        int, Field(default=5, ge=1)
    ],
):
    """Analyze messages and return the n hottest topics along with related conversations."""


@app.get(
    "/analytics/topic/{topic}",
    summary="Get conversations for topic",
    description="Analyze conversations/messages and return conversations referring to the given topic.",
)
def analyze_message_hot_topics(
    topic: str,
):
    """Analyze messages and return conversations referring to the given topic."""

@app.get(
    '/conversations',
    summary="Get conversations",
)
def get_conversations():
    """Get all conversations."""


@app.get("/health")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status=HealthStatus.HEALTHY)
