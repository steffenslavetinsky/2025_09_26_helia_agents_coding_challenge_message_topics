from enum import Enum


from pydantic import BaseModel as PydBaseModel
from pydantic.alias_generators import to_camel
from typing import TypeAlias


class BaseModel(PydBaseModel):
    class Config:
        alias_generator = to_camel
        validate_by_name = True


class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheckResponse(BaseModel):
    status: HealthStatus = HealthStatus.UNHEALTHY


ConversationId: TypeAlias = str
TopicId: TypeAlias = str
MessageContent: TypeAlias = str
TopicName: TypeAlias = str


class MessageRole(Enum):
    GUEST = "guest"
    AGENT = "agent"
class Message(BaseModel):
    role: MessageRole
    content: MessageContent

class Conversation(BaseModel):
    id: ConversationId
    messages: list[Message]

class Topic(BaseModel):
    id: TopicId
    description: TopicName

class AllowedTopics(BaseModel):
    topics: list[Topic]

class ConversationTopics(BaseModel):
    conversation_id: ConversationId
    topics: list[TopicId]