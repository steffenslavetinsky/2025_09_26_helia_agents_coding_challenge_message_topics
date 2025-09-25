TOPIC_LABELING_PROMPT = """
Analyze the following hotel guest conversation and identify ALL relevant topics from the allowed list. Return a JSON object with a "topics" array containing the topic IDs.

IMPORTANT INSTRUCTIONS:
- No matter what language the conversation is in, you MUST return topic IDs in English from the allowed list
- Use only the exact TOPIC_ID strings from the allowed list below
- Multiple topics can be identified for a single conversation
- Return topics as an array even if there's only one topic

ALLOWED TOPICS:
{topics_list}

EXAMPLES:

Example 1:
Conversation:
User: Hi, I need to cancel my reservation for next week
Agent: I can help you with that. Can you provide me with your confirmation number?
User: It's ABC123. I have a family emergency and can't travel

Expected JSON Response:
{{"topics": ["booking_management"]}}

Example 2:
Conversation:
User: What time is check-in? I'm arriving early tomorrow
Agent: Check-in is at 3 PM, but I can see if we have your room ready earlier
User: That would be great, I have a 2 PM meeting nearby

Expected JSON Response:
{{"topics": ["arrival_departure"]}}

Example 3:
Conversation:
User: I was charged twice for my stay, can you help?
Agent: I apologize for the confusion. Let me look into your billing
User: I have the receipt showing the duplicate charge
Agent: I'll also need to coordinate with housekeeping to ensure your room is ready

Expected JSON Response:
{{"topics": ["billing_payments", "housekeeping"]}}

Now analyze this conversation:
{conversation_text}

Return only valid JSON with topic IDs from the allowed list above. Use exact TOPIC_ID strings.
"""