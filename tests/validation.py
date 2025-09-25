from typing import List, Dict


def expect_conversation_response(response, expected_count: int = None):
    """Helper to validate conversation response structure"""
    assert response.status_code == 200
    conversations = response.json()
    assert isinstance(conversations, list)
    if expected_count is not None:
        assert len(conversations) == expected_count
    return conversations


def expect_hot_topics_response(response, expected_count: int = None):
    """Helper to validate hot topics response structure"""
    assert response.status_code == 200
    hot_topics = response.json()
    assert isinstance(hot_topics, list)
    if expected_count is not None:
        assert len(hot_topics) == expected_count
    return hot_topics


def validate_conversation_content(actual_conversation: Dict, expected_conversation: Dict):
    """Validate that actual conversation matches expected conversation content"""
    assert actual_conversation["id"] == expected_conversation["id"]
    assert len(actual_conversation["messages"]) == len(expected_conversation["messages"])

    for actual_msg, expected_msg in zip(actual_conversation["messages"], expected_conversation["messages"]):
        assert actual_msg["role"] == expected_msg["role"]
        assert actual_msg["content"] == expected_msg["content"]


def find_conversation_by_id(conversations: List[Dict], conversation_id: str) -> Dict:
    """Find conversation in list by ID"""
    for conv in conversations:
        if conv["id"] == conversation_id:
            return conv
    raise AssertionError(f"Conversation with ID {conversation_id} not found in response")


def expect_conversations_contain(response_conversations: List[Dict], expected_conversations: List[Dict]):
    """Validate that response contains all expected conversations with correct content"""
    assert len(response_conversations) == len(expected_conversations)

    for expected_conv in expected_conversations:
        actual_conv = find_conversation_by_id(response_conversations, expected_conv["id"])
        validate_conversation_content(actual_conv, expected_conv)