from services import ConversationService, TopicService
from outbound import InMemoryConversationRepository, InMemoryTopicRepository, OpenAITopicLabeler
import json
from pydantic import BaseSettings
from app.models import Conversation, Message, Topic


class Settings(BaseSettings):
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()


class UUID:
    @staticmethod
    def generate() -> str:
        import uuid
        return str(uuid.uuid4())
    

allowed_topics = [
    {"id": "booking_management", "description": "Reservations, changes, cancellations, pricing inquiries"},
    {"id": "pre_arrival", "description": "Requests and updates before arrival"},
    {"id": "arrival_departure", "description": "Check-in, check-out, extensions, timing issues"},
    {"id": "transport", "description": "Shuttles, taxis, parking, travel logistics"},
    {"id": "billing_payments", "description": "Invoices, payments, deposits, refunds, charges"},
    {"id": "room_requests", "description": "Beds, cots, pets, amenities, in-room needs"},
    {"id": "housekeeping", "description": "Cleaning, linens, turndown, room readiness"},
    {"id": "maintenance_it", "description": "Wi-Fi, appliances, room maintenance, technical issues"},
    {"id": "amenities", "description": "Pool, gym, spa, leisure facilities"},
    {"id": "food_drink", "description": "Breakfast, dining, room service, dietary needs"},
    {"id": "concierge_activities", "description": "Recommendations, bookings, tours, local guidance"},
    {"id": "family_kids", "description": "Childcare, activities, baby equipment"},
    {"id": "accessibility", "description": "Mobility, accessible rooms, special assistance"},
    {"id": "safety_security", "description": "Keys, lost items, safety, emergencies"},
    {"id": "guest_communications", "description": "Wake-up calls, messaging, feedback, general inquiries"},
    {"id": "events_meetings", "description": "Meetings, events, AV, catering, group services"}
]


class ServiceFactory:

    def __init__(self):
        self.conversation_repository = InMemoryConversationRepository()
        self.topic_repository = InMemoryTopicRepository()
        self.topic_labeler = OpenAITopicLabeler()
        self.conversation_service = ConversationService(self.conversation_repository)
        self.topic_service = TopicService(self.topic_repository, self.conversation_repository, self.topic_labeler)

        if settings.environment == 'development':
            self._local_initialize()

    def create_conversation_service(self) -> ConversationService:
        return self.conversation_service

    def create_topic_service(self) -> TopicService:
        return self.topic_service
    
    def _local_initialize(self) -> None:
        self._read_conversation_data_from_disk_to_repository(self.conversation_repository)
        self._initialize_allowed_topics(self.topic_repository)
        self._initialize_topics(self.conversation_service, self.topic_service)
    
    def _read_conversation_data_from_disk_to_repository(self, conversation_repository: InMemoryConversationRepository) -> None:

        with open('data/conversations.json', 'r') as f:
            conversations_data = json.load(f)
            for conversation_dict in conversations_data:
                conversation = Conversation(id=UUID.generate(), messages=[Message(**msg) for msg in conversation_dict['messages']])
                conversation_repository.add(conversation)

    def _initialize_allowed_topics(self, topic_repository: InMemoryTopicRepository) -> None:
        topics = [Topic(id=topic['id'], description=topic['description']) for topic in allowed_topics]
        topic_repository.initialize_allowed_topics(topics)

    def _initialize_topics(self, conversation_service: ConversationService, topic_service: TopicService) -> None:
        conversations = conversation_service.get_all_conversations()
        for conversation in conversations:
            topic_service.add_topic_for_conversation(conversation.id)
