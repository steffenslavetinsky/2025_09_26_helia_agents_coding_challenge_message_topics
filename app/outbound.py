
from typing import Dict, List, Optional
from collections import defaultdict
import json
import os
from openai import OpenAI
from app.apis import ConversationRepositoryAPI, TopicRepositoryAPI, TopicLabelerAPI
from app.models import Conversation, TopicId, Topic, ConversationId, Message, MessageRole, BaseModel
from app.topic_labeler_prompt import TOPIC_LABELING_PROMPT


class DBConversation(BaseModel):
    _id: ConversationId
    messages: List[Dict]


class DBTopic(BaseModel):
    _id: TopicId
    description: str


class DBMessage(BaseModel):
    role: str
    content: str


def _conversation_convert_to_db(self) -> Dict:
    return DBConversation(
        _id=self.id,
        messages=[msg.convert_to_db() for msg in self.messages]
    ).model_dump()


def _topic_convert_to_db(self) -> Dict:
    return DBTopic(
        _id=self.id,
        description=self.description
    ).model_dump()


def _message_convert_to_db(self) -> Dict:
    return DBMessage(
        role=self.role.value,
        content=self.content
    ).model_dump()


Conversation.convert_to_db = _conversation_convert_to_db
Topic.convert_to_db = _topic_convert_to_db
Message.convert_to_db = _message_convert_to_db


class InMemoryConversationRepository(ConversationRepositoryAPI):
    def __init__(self):
        self._conversations: Dict[ConversationId, Dict] = {}

    def get_all_conversations(self) -> List[Conversation]:
        return [self._from_db_conversation(conv) for conv in self._conversations.values()]

    def get_many(self, conversation_ids: List[ConversationId]) -> List[Conversation]:
        result = []
        for conv_id in conversation_ids:
            if conv_id in self._conversations:
                result.append(self._from_db_conversation(self._conversations[conv_id]))
        return result

    def get_by_id(self, conversation_id: ConversationId) -> Optional[Conversation]:
        if conversation_id in self._conversations:
            return self._from_db_conversation(self._conversations[conversation_id])
        return None

    def add(self, conversation: Conversation) -> None:
        self._conversations[conversation.id] = conversation.convert_to_db()

    def _from_db_conversation(self, db_conv: Dict) -> Conversation:
        messages = [
            Message(
                role=MessageRole(msg['role']),
                content=msg['content']
            )
            for msg in db_conv['messages']
        ]
        return Conversation(
            id=db_conv['_id'],
            messages=messages
        )


class InMemoryTopicRepository(TopicRepositoryAPI):
    def __init__(self):
        self._topics: Dict[TopicId, Dict] = {}
        self._conversation_topics: Dict[ConversationId, List[TopicId]] = defaultdict(list)
        self._topic_conversations: Dict[TopicId, List[ConversationId]] = defaultdict(list)

    def get_all_topics(self) -> List[Topic]:
        return [self._from_db_topic(topic) for topic in self._topics.values()]

    def add_topic_for_conversation(self, conversation_id: ConversationId, topic_id: TopicId) -> None:
        if topic_id not in self._conversation_topics[conversation_id]:
            self._conversation_topics[conversation_id].append(topic_id)
        if conversation_id not in self._topic_conversations[topic_id]:
            self._topic_conversations[topic_id].append(conversation_id)

    def get_conversations_by_topic(self, topic_id: TopicId) -> List[ConversationId]:
        return self._topic_conversations[topic_id].copy()

    def get_n_hottest_topics(self, n: int) -> List[TopicId]:
        topic_counts = [
            (topic_id, len(conversations))
            for topic_id, conversations in self._topic_conversations.items()
        ]
        topic_counts.sort(key=lambda x: x[1], reverse=True)
        return [topic_id for topic_id, _ in topic_counts[:n]]

    def initialize_allowed_topics(self, topics: List[Topic]) -> None:
        for topic in topics:
            self._topics[topic.id] = topic.convert_to_db()

    def _from_db_topic(self, db_topic: Dict) -> Topic:
        return Topic(
            id=db_topic['_id'],
            description=db_topic['description']
        )


class OpenAITopicLabeler(TopicLabelerAPI):
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def label_conversation(self, conversation: Conversation, allowed_topics: List[Topic]) -> TopicId:
        if not allowed_topics:
            raise ValueError("No allowed topics provided")

        # Format conversation for prompt
        conversation_text = self._format_conversation(conversation)

        # Create the prompt with few-shot examples
        prompt = self._create_prompt(conversation_text, allowed_topics)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-2025-04-14",
                messages=[
                    {"role": "system", "content": "You are an expert hotel conversation topic classifier. Analyze hotel guest conversations and identify the most relevant topic from the provided list."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            # Parse and validate response
            result = json.loads(response.choices[0].message.content)
            topics = result.get("topics", [])
            return self._validate_and_get_primary_topic(topics, allowed_topics)

        except Exception as e:
            # Fallback to first topic if API call fails
            print(f"OpenAI API error: {e}")
            return allowed_topics[0].id if allowed_topics else ""

    def _format_conversation(self, conversation: Conversation) -> str:
        formatted = []
        for msg in conversation.messages:
            role = "Customer" if msg.role == MessageRole.USER else "Agent"
            formatted.append(f"{role}: {msg.content}")
        return "\n".join(formatted)

    def _create_prompt(self, conversation_text: str, allowed_topics: List[Topic]) -> str:
        topics_list = "\n".join([f"- TOPIC_ID: {topic.id} | Description: {topic.description}" for topic in allowed_topics])
        return TOPIC_LABELING_PROMPT.format(
            topics_list=topics_list,
            conversation_text=conversation_text
        )


    def _validate_and_get_primary_topic(self, topics: List[str], allowed_topics: List[Topic]) -> TopicId:
        allowed_ids = {topic.id for topic in allowed_topics}

        # Find first valid topic from the list
        for topic in topics:
            if topic in allowed_ids:
                return topic

        # Fallback to first allowed topic if no valid topics found
        return allowed_topics[0].id if allowed_topics else ""
