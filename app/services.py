

from app.apis import ConversationRepositoryAPI, TopicRepositoryAPI, TopicLabelerAPI
from app.models import Conversation, TopicId, Topic, ConversationId



class ConversationService:
    def __init__(self, conversation_repository: ConversationRepositoryAPI):
        self.conversation_repository = conversation_repository

    def get_all_conversations(self)-> list[Conversation]:
        return self.conversation_repository.get_all_conversations()

    def get_conversation_by_ids(self, conversation_ids: list[ConversationId]) -> list[Conversation]:
        return self.conversation_repository.get_many(conversation_ids)
    

class TopicService:
    def __init__(self, topic_repository: TopicRepositoryAPI, conversation_repository: ConversationRepositoryAPI, topic_labeler: TopicLabelerAPI):
        self.topic_repository = topic_repository
        self.conversation_repository = conversation_repository
        self.topic_labeler = topic_labeler

    def add_topic_for_conversation(self, conversation_id: ConversationId) -> None:
        conversation = self.conversation_repository.get_by_id(conversation_id)
        allowed_topics = self.topic_repository.get_all_topics()
        topic_id = self.topic_labeler.label_conversation(conversation, allowed_topics)
        self.topic_repository.add_topic_for_conversation(conversation_id, topic_id)
        

    def get_conversations_by_topic(self, topic_id: str) -> list[Conversation]:
        self._validate_topic_exists(topic_id)
        conversation_ids = self.topic_repository.get_conversations_by_topic(topic_id)
        return self.conversation_repository.get_many(conversation_ids)

    def get_hot_topics(self, n: int) -> dict[TopicId, list[Conversation]]:
        hot_topics = self.topic_repository.get_n_hottest_topics(n)
        hot_topics_break_ties = sorted(hot_topics)[:n]
        return {topic_id: self.get_conversations_by_topic(topic_id) for topic_id in hot_topics_break_ties}
    
    def _validate_topic_exists(self, topic_id: TopicId) -> None:
        allowed_topics = self.topic_repository.get_all_topics()
        if topic_id not in [topic.id for topic in allowed_topics]:
            raise ValueError(f"Topic {topic_id} does not exist.")
