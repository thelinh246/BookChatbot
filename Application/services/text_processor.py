from deep_translator import GoogleTranslator
from langdetect import detect
import re
import unicodedata

class TextProcessor:
    def __init__(self):
        self.translator_vi_to_en = GoogleTranslator(source='vi', target='en')
        self.translator_en_to_vi = GoogleTranslator(source='en', target='vi')

    def normalize_author_name(self, name: str) -> str:
        name = name.lower()
        return ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')

    def translate_query(self, query: str) -> str:
        try:
            return self.translator_vi_to_en.translate(query)
        except Exception:
            return query

    def get_translated_info(self, text: str, author_name: str) -> tuple[str, str]:
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        filtered = [s for s in sentences if len(s.split()) > 3 and not re.match(r'^\d+\.\s*(\d+\.\s*)*$', s)]
        main_text = " ".join(filtered or ["Không có thông tin."])
        lang = detect(main_text) if main_text else 'en'
        if lang == 'vi':
            vietnamese_text = main_text
            english_text = self.translator_vi_to_en.translate(vietnamese_text) or "Không thể dịch."
        else:
            english_text = main_text
            vietnamese_text = self.translator_en_to_vi.translate(english_text) or "Không thể dịch."
        return "\n".join(re.split(r'(?<=[.!?])\s+', vietnamese_text.strip())), "\n".join(re.split(r'(?<=[.!?])\s+', english_text.strip()))