
class TestTopics:
    BOOKING_MANAGEMENT = "booking_management"
    TRANSPORT = "transport"
    FOOD_DRINK = "food_drink"
    PRE_ARRIVAL = "pre_arrival"
    AMENITIES = "amenities"


class TestConversations:
    BOOKING_1 = {
        "id": "conv-booking-001",
        "topic_id": TestTopics.BOOKING_MANAGEMENT,
        "messages": [
            {"role": "guest", "content": "I need to cancel my reservation for tomorrow"},
            {"role": "agent", "content": "I'll help you cancel your reservation"}
        ]
    }

    BOOKING_2 = {
        "id": "conv-booking-002",
        "topic_id": TestTopics.BOOKING_MANAGEMENT,
        "messages": [
            {"role": "guest", "content": "Can I modify my booking dates?"},
            {"role": "agent", "content": "I can help you change your reservation dates"}
        ]
    }

    TRANSPORT_1 = {
        "id": "conv-transport-001",
        "topic_id": TestTopics.TRANSPORT,
        "messages": [
            {"role": "guest", "content": "Do you have airport shuttle service?"},
            {"role": "agent", "content": "Yes, we offer complimentary shuttle service"}
        ]
    }

    TRANSPORT_2 = {
        "id": "conv-transport-002",
        "topic_id": TestTopics.TRANSPORT,
        "messages": [
            {"role": "guest", "content": "Where can I park my car?"},
            {"role": "agent", "content": "We have valet parking available in the main entrance"}
        ]
    }

    FOOD = {
        "id": "conv-food-001",
        "topic_id": TestTopics.FOOD_DRINK,
        "messages": [
            {"role": "guest", "content": "What time is breakfast served?"},
            {"role": "agent", "content": "Breakfast is served from 6 AM to 10 AM"}
        ]
    }
