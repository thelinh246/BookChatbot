import streamlit as st
from config import load_config
from database import MySQLClient, RedisClient
from services import BookRecommender, ConversationManager
from workflows import ChatbotWorkflow
from ui import StreamlitUI

def main():
    config = load_config()
    
    # Truyền config["mysql"] cho MySQLClient
    mysql_client = MySQLClient(config["mysql"])
    redis_client = RedisClient(config["redis"]["host"], config["redis"]["port"], config["redis"]["password"])
    
    df = mysql_client.load_data()
    recommender = BookRecommender(df)
    conversation_manager = ConversationManager(redis_client)
    workflow = ChatbotWorkflow(config["openai"], df, recommender)  # Truyền config["openai"]
    ui = StreamlitUI(workflow, conversation_manager)
    ui.run()
    
    mysql_client.close()

if __name__ == "__main__":
    main()