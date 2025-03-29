from deep_translator import GoogleTranslator

def translate_vi_to_en(text: str) -> str:
    translator = GoogleTranslator(source='vi', target='en')
    try:
        return translator.translate(text)
    except Exception:
        return text

def translate_en_to_vi(text: str) -> str:
    translator = GoogleTranslator(source='en', target='vi')
    try:
        return translator.translate(text)
    except Exception:
        return text