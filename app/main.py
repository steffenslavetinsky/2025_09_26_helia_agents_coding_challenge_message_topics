from fastapi import FastAPI, Depends
from app.models import HealthCheckResponse, HealthStatus, Conversation
from typing import Annotated, List, Dict
from pydantic import Field
from app.service_factory import ServiceFactory
from app.services import ConversationService, TopicService

app = FastAPI()
service_factory = ServiceFactory()

conversation_service = service_factory.create_conversation_service()
topic_service = service_factory.create_topic_service()

def get_conversation_service() -> ConversationService:
    return conversation_service

def get_topic_service() -> TopicService:
    return topic_service

@app.get(
    "/analytics/hot-topics",
    summary="Get hot topics from messages",
    description="Analyze conversations/messages and return the n hottest topics along with related conversations.",
    response_model=List[Dict]
)
def analyze_message_hot_topics(
    number_of_topics: Annotated[
        int, Field(default=5, ge=1)
    ],
    topic_service: TopicService = Depends(get_topic_service)
) -> List[Dict]:
    """Analyze messages and return the n hottest topics along with related conversations."""
    hot_topics = topic_service.get_hot_topics(number_of_topics)
    return [{"topic": topic, "conversations": conversations} for topic, conversations in hot_topics.items()]
    


@app.get(
    "/analytics/topic/{topic}",
    summary="Get conversations for topic",
    description="Analyze conversations/messages and return conversations referring to the given topic.",
    response_model=List[Conversation]
)
def get_conversations_for_topic(
    topic: str,
    topic_service: TopicService = Depends(get_topic_service)
) -> List[Conversation]:
    """Analyze messages and return conversations referring to the given topic."""
    conversations = topic_service.get_conversations_by_topic(topic)
    return conversations


@app.get(
    '/conversations',
    summary="Get conversations",
    response_model=List[Conversation]
)
def get_conversations(
    conversation_service: ConversationService = Depends(get_conversation_service)
) -> List[Conversation]:
    """Get all conversations."""
    return conversation_service.get_all_conversations()


@app.get("/health")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status=HealthStatus.HEALTHY)
