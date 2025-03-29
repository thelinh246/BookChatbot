from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import logging
from utils.translation import translate_vi_to_en
from utils.text_normalization import normalize_text
import re

class IntentClassifier:
    def __init__(self, api_key):
        self.api_key = api_key
        self.intents = ['lời chào', 'tìm sách', 'tìm thông tin tác giả', 'chủ đề khác']

    def classify(self, user_input: str) -> str:
        user_input = normalize_text(translate_vi_to_en(user_input))
        prompt = f"""Phân loại ý định của câu sau thành một trong: {', '.join(self.intents)}.
            Chỉ trả về tên intent.
            Câu: "{user_input}"
            """
        try:
            llm = ChatOpenAI(model="gpt-4", api_key=self.api_key)
            response = llm.invoke([HumanMessage(content=prompt)])
            intent = response.content.strip()
            return intent if intent in self.intents else "chủ đề khác"
        except Exception as e:
            logging.error(f"Lỗi phân loại intent: {e}")
            return self._classify_fallback(user_input)

    def _classify_fallback(self, user_input: str) -> str:
        if re.search(r'\b(hi|hello)\b', user_input): return 'lời chào'
        if re.search(r'\b(book|books)\b', user_input): return 'tìm sách'
        if re.search(r'\b(author|information)\b', user_input): return 'tìm thông tin tác giả'
        return 'chủ đề khác'