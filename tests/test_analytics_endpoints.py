import pytest
from fastapi.testclient import TestClient
from app.main import app, get_conversation_service, get_topic_service
from tests.service_factory import MockServiceFactory
from tests.data import TestConversations, TestTopics
from tests.setup import (
    setup_conversations_in_service
)
from tests.validation import expect_hot_topics_response, expect_conversations_contain


@pytest.fixture
def test_client():
    """Create test client with dependency overrides"""
    test_service_factory = MockServiceFactory()
    test_service_factory.setup_test_data()
    topic_service = test_service_factory.create_topic_service()
    conversation_service = test_service_factory.create_conversation_service()

    # Override dependencies
    app.dependency_overrides[get_conversation_service] = lambda: conversation_service
    app.dependency_overrides[get_topic_service] = lambda: topic_service

    yield TestClient(app), test_service_factory

    # Cleanup
    app.dependency_overrides.clear()


def test_hot_topics_with_conversations(test_client):
    """Should return hot topics ordered by conversation count"""
    client, service_factory = test_client

    # Setup: Create conversations with different topics
    conversations_data = [
        TestConversations.FOOD,
        TestConversations.BOOKING_1,
        TestConversations.BOOKING_2,
        TestConversations.TRANSPORT_1,
        TestConversations.TRANSPORT_2,
    ]
    setup_conversations_in_service(service_factory, conversations_data)


    response = client.get("/analytics/hot-topics?number_of_topics=2")


    hot_topics = expect_hot_topics_response(response)
    assert len(hot_topics) == 2
    assert TestTopics.BOOKING_MANAGEMENT in [topic["topic"] for topic in hot_topics]
    assert TestTopics.TRANSPORT in [topic["topic"] for topic in hot_topics]
    expect_conversations_contain(hot_topics[0]["conversations"], [TestConversations.BOOKING_1, TestConversations.BOOKING_2])
    expect_conversations_contain(hot_topics[1]["conversations"], [TestConversations.TRANSPORT_1, TestConversations.TRANSPORT_2])



def test_conversations_for_existing_topic(test_client):
    """Should return conversations for existing topic"""
    client, service_factory = test_client
    conversations_data = [TestConversations.BOOKING_1, TestConversations.TRANSPORT_1]
    setup_conversations_in_service(service_factory, conversations_data)


    response = client.get(f"/analytics/topic/{TestTopics.BOOKING_MANAGEMENT}")


    assert response.status_code == 200
    conversations = response.json()
    expect_conversations_contain(conversations, [TestConversations.BOOKING_1])


def test_conversations_for_topic_not_found(test_client):
    """Should return empty list for non-existent topic"""
    client, service_factory = test_client
    conversations_data = [TestConversations.BOOKING_1, TestConversations.TRANSPORT_1]
    setup_conversations_in_service(service_factory, conversations_data)


    response = client.get(f"/analytics/topic/{TestTopics.FOOD_DRINK}")


    assert response.status_code == 200
    conversations = response.json()
    assert isinstance(conversations, list)
    assert len(conversations) == 0