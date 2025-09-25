from typing import List, Dict
from app.models import Conversation, Message, MessageRole
from tests.service_factory import MockServiceFactory


def create_test_conversation(conversation_id: str, messages: List[Dict[str, str]]) -> Conversation:
    """Create a test conversation with readable message format"""
    msg_objects = [
        Message(
            role=MessageRole.GUEST if msg["role"] == "guest" else MessageRole.AGENT,
            content=msg["content"]
        )
        for msg in messages
    ]
    return Conversation(id=conversation_id, messages=msg_objects)


def setup_conversations_in_service(service_factory: MockServiceFactory, conversations_data: List[Dict]) -> List[str]:
    """Setup multiple conversations in repository and return their IDs"""
    conversation_ids = []
    for conv_data in conversations_data:
        conversation = create_test_conversation(conv_data["id"], conv_data["messages"])
        service_factory.conversation_repository.add(conversation)
        conversation_ids.append(conversation.id)

    topic_mapping = create_topic_mapping_from_conversations(conversations_data)
    setup_topics_for_conversations(service_factory, topic_mapping)
    return conversation_ids


def setup_topics_for_conversations(service_factory: MockServiceFactory, conversation_topic_mapping: Dict[str, str]):
    """Setup topics for conversations using the mock labeler with flexible mapping"""
    # Set up the mock labeler with the mapping
    for conv_id, topic_id in conversation_topic_mapping.items():
        service_factory.topic_labeler.set_topic_for_conversation(conv_id, topic_id)
        service_factory.topic_service.add_topic_for_conversation(conv_id)


def setup_single_topic_for_conversations(service_factory: MockServiceFactory, conversation_ids: List[str], topic_id: str = "booking_management"):
    """Setup same topic for multiple conversations - convenience helper"""
    mapping = {conv_id: topic_id for conv_id in conversation_ids}
    setup_topics_for_conversations(service_factory, mapping)


def create_topic_mapping_from_conversations(conversations_data: List[Dict]) -> Dict[str, str]:
    """Create topic mapping dict from list of conversation objects using their topic_id"""
    return {conv["id"]: conv["topic_id"] for conv in conversations_data}