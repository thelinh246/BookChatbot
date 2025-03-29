import redis
import json
import uuid

class RedisClient:
    def __init__(self, host, port, password):
        self.client = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def save_conversation(self, session_id: str, messages: list):
        title = next((msg["content"] for msg in messages if msg["role"] == "user"), "Untitled Session")
        self.client.set(session_id, json.dumps({"title": title, "messages": messages}))
        self.client.zadd("session_order", {session_id: int(uuid.uuid4().int % 1e9)})

    def load_conversation(self, session_id: str) -> list:
        data = self.client.get(session_id)
        if data:
            self.client.zadd("session_order", {session_id: int(uuid.uuid4().int % 1e9)})
            return json.loads(data)["messages"]
        return []

    def delete_conversation(self, session_id: str):
        self.client.delete(session_id)
        self.client.zrem("session_order", session_id)

    def get_all_sessions(self):
        session_ids = self.client.zrevrange("session_order", 0, -1)
        return [{"id": sid, "title": json.loads(self.client.get(sid)).get("title", "Untitled Session")} for sid in session_ids]