class ConversationManager:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def save(self, session_id: str, messages: list):
        self.redis_client.save_conversation(session_id, messages)

    def load(self, session_id: str) -> list:
        return self.redis_client.load_conversation(session_id)

    def delete(self, session_id: str):
        self.redis_client.delete_conversation(session_id)

    def get_sessions(self):
        return self.redis_client.get_all_sessions()