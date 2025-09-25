from fastapi import FastAPI
from app.models import HealthCheckResponse, HealthStatus
from typing import Annotated
from pydantic import Field
from service_factory import ServiceFactory

app = FastAPI()

conversation_service = ServiceFactory.create_conversation_service()
topic_service = ServiceFactory.create_topic_service()

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
    hot_topics = topic_service.get_hot_topics(number_of_topics)
    return hot_topics
    


@app.get(
    "/analytics/topic/{topic}",
    summary="Get conversations for topic",
    description="Analyze conversations/messages and return conversations referring to the given topic.",
)
def get_conversations_for_topic(
    topic: str,
):
    """Analyze messages and return conversations referring to the given topic."""
    conversations = topic_service.get_conversations_for_topic(topic)
    return conversations


@app.get(
    '/conversations',
    summary="Get conversations",
)
def get_conversations():
    """Get all conversations."""
    return conversation_service.get_all_conversations()


@app.get("/health")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status=HealthStatus.HEALTHY)
