
from app.apis import ConversationRepositoryAPI, TopicRepositoryAPI, TopicLabelerAPI
from app.models import Conversation, TopicId, Topic, ConversationId

class InMemoryConversationRepository(ConversationRepositoryAPI):
    pass

class InMemoryTopicRepository(TopicRepositoryAPI):
    pass

class OpenAITopicLabeler(TopicLabelerAPI):
    pass
