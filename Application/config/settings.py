from dotenv import load_dotenv
import os

def load_config():
    load_dotenv()
    return {
        "mysql": {
            "user": "root",
            "password": "123456",
            "host": "localhost",
            "database": "book_db"
        },
        "redis": {
            "host": os.getenv("REDIS_HOST"),
            "port": int(os.getenv("REDIS_PORT", 6379)),
            "password": os.getenv("REDIS_PASSWORD")
        },
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    }