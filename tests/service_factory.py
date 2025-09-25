from typing import List
from app.services import ConversationService, TopicService
from app.outbound import InMemoryConversationRepository, InMemoryTopicRepository
from app.apis import TopicLabelerAPI
from app.models import Conversation, Topic, TopicId


class MockTopicLabeler(TopicLabelerAPI):
    def __init__(self, topic_mapping: dict = None):
        """
        topic_mapping: dict mapping conversation_id -> topic_id
        If not provided, defaults to "booking_management" for all conversations
        """
        self.topic_mapping = topic_mapping or {}
        self.default_topic = "booking_management"

    def label_conversation(self, conversation: Conversation, allowed_topics: List[Topic]) -> TopicId:
        # Return mapped topic for this conversation, or default
        if conversation.id in self.topic_mapping:
            return self.topic_mapping[conversation.id]
        return self.default_topic

    def set_topic_for_conversation(self, conversation_id: str, topic_id: str):
        """Helper to set topic mapping during tests"""
        self.topic_mapping[conversation_id] = topic_id


class MockServiceFactory:
    def __init__(self, mock_topic_labeler: MockTopicLabeler = None):
        self.conversation_repository = InMemoryConversationRepository()
        self.topic_repository = InMemoryTopicRepository()
        self.topic_labeler = mock_topic_labeler or MockTopicLabeler()
        self.conversation_service = ConversationService(self.conversation_repository)
        self.topic_service = TopicService(self.topic_repository, self.conversation_repository, self.topic_labeler)

        # Don't auto-initialize like the real ServiceFactory - tests control this

    def create_conversation_service(self) -> ConversationService:
        return self.conversation_service

    def create_topic_service(self) -> TopicService:
        return self.topic_service

    def setup_test_data(self):
        """Helper to setup minimal test data"""
        from tests.data import TestTopics
        # Initialize test topics
        test_topics = [
            Topic(id=TestTopics.BOOKING_MANAGEMENT, description="Booking management"),
            Topic(id=TestTopics.TRANSPORT, description="Transport services"),
            Topic(id=TestTopics.FOOD_DRINK, description="Food and drink"),
            Topic(id=TestTopics.PRE_ARRIVAL, description="Pre-arrival services"),
            Topic(id=TestTopics.AMENITIES, description="Hotel amenities"),
        ]
        self.topic_repository.initialize_allowed_topics(test_topics)