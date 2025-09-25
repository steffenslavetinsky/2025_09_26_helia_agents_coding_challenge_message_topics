import pytest
from fastapi.testclient import TestClient
from app.main import app, get_conversation_service, get_topic_service
from tests.service_factory import MockServiceFactory
from tests.data import TestConversations
from tests.setup import setup_conversations_in_service
from tests.validation import expect_conversation_response, expect_conversations_contain


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


def test_get_conversations_when_empty(test_client):
    """Should return empty list when no conversations exist"""
    client, service_factory = test_client

    response = client.get("/conversations")

    _ = expect_conversation_response(response, expected_count=0)


def test_get_conversations_with_data(test_client):
    """Should return all conversations when they exist"""
    client, service_factory = test_client

    # Setup: Add conversations
    conversations_data = [TestConversations.BOOKING_1, TestConversations.TRANSPORT_1]
    setup_conversations_in_service(service_factory, conversations_data)

    response = client.get("/conversations")

    conversations = expect_conversation_response(response, expected_count=2)
    expect_conversations_contain(conversations, conversations_data)