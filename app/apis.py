
from abc import ABC, abstractmethod
from app.models import Conversation, TopicId, Topic, ConversationId
class ConversationRepositoryAPI(ABC):
    @abstractmethod
    def get_all_conversations(self) -> list[Conversation]:
        pass

    @abstractmethod
    def get_many(self, conversation_ids) -> list[Conversation]:
        pass

    @abstractmethod
    def get_by_id(self, conversation_id) -> Conversation:
        pass

class TopicRepositoryAPI(ABC):
    @abstractmethod
    def get_all_topics(self) -> list[Topic]:
        pass

    @abstractmethod
    def add_topic_for_conversation(self, conversation_id: ConversationId, topic_id: TopicId) -> None:
        pass

    @abstractmethod
    def get_conversations_by_topic(self, topic_id: TopicId) -> list[ConversationId]:
        pass

    @abstractmethod
    def get_n_hottest_topics(self, n: int) -> list[TopicId]:
        pass

class TopicLabelerAPI(ABC):
    @abstractmethod
    def label_conversation(self, conversation, allowed_topics) -> TopicId:
        pass