from langgraph.graph import StateGraph, END
from models import GraphState
from services import IntentClassifier, BookRecommender, AuthorInfoSearcher, TextProcessor
import re

class ChatbotWorkflow:
    def __init__(self, openai_config, df, recommender):
        self.classifier = IntentClassifier(openai_config["api_key"])
        self.recommender = recommender
        self.searcher = AuthorInfoSearcher()
        self.processor = TextProcessor()
        self.df = df
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(GraphState)
        
        # Các node
        workflow.add_node("classify_intent", self.classify_intent)
        workflow.add_node("extract_author", self.extract_author)
        workflow.add_node("extract_book_title", self.extract_book_title)
        workflow.add_node("search_author_info", self.search_author_info)
        workflow.add_node("recommend_books", self.recommend_books)
        workflow.add_node("handle_greeting", self.handle_greeting)
        workflow.add_node("handle_author_info", self.handle_author_info)
        workflow.add_node("handle_book_recommendation", self.handle_book_recommendation)
        workflow.add_node("handle_book_description", self.handle_book_description)
        workflow.add_node("handle_other_intents", self.handle_other_intents)

        # Điểm bắt đầu
        workflow.set_entry_point("classify_intent")

        # Điều kiện chuyển tiếp
        workflow.add_conditional_edges(
            "classify_intent",
            lambda state: state["intent"],
            {
                "lời chào": "handle_greeting",
                "tìm sách": "recommend_books",
                "tìm thông tin tác giả": "extract_author",
                "chủ đề khác": "handle_other_intents"
            }
        )
        workflow.add_edge("extract_author", "search_author_info")
        workflow.add_edge("search_author_info", "handle_author_info")
        workflow.add_edge("extract_book_title", "handle_book_description")
        workflow.add_edge("recommend_books", "handle_book_recommendation")
        workflow.add_edge("handle_greeting", END)
        workflow.add_edge("handle_author_info", END)
        workflow.add_edge("handle_book_recommendation", END)
        workflow.add_edge("handle_book_description", END)
        workflow.add_edge("handle_other_intents", END)

        return workflow.compile()

    def classify_intent(self, state: GraphState) -> GraphState:
        user_input = self.processor.translate_query(state["user_input"].lower())
        return {"intent": self.classifier.classify(user_input)}

    def extract_author(self, state: GraphState) -> GraphState:
        user_input = state["user_input"].lower()
        match = re.search(r"tác giả\s+([^\n]+)", user_input)
        author_name = match.group(1).strip() if match else user_input.strip()
        return {"author_name": author_name}

    def extract_book_title(self, state: GraphState) -> GraphState:
        user_input = state["user_input"].lower()
        match = re.search(r"(?:mô tả sách|nội dung sách|description of)\s+(.+)", user_input)
        book_title = match.group(1).strip() if match else user_input.strip()
        return {"book_title": book_title}

    def search_author_info(self, state: GraphState) -> GraphState:
        author_name = state["author_name"]
        if not author_name:
            return {"author_info": "Không tìm thấy tên tác giả trong yêu cầu."}
        author_info = self.searcher.search(author_name)
        return {"author_info": author_info}

    def recommend_books(self, state: GraphState) -> GraphState:
        query = state["user_input"]
        translated_query = self.processor.translate_query(query)
        recommendations = self.recommender.recommend(translated_query)
        return {"recommendations": recommendations}

    def handle_greeting(self, state: GraphState) -> GraphState:
        return {"response": "👋 Chào bạn! Tôi là chatbot gợi ý sách. Bạn khỏe không? Có thể hỏi tôi về sách, tác giả, hoặc chỉ chào hỏi thôi cũng được!"}

    def handle_author_info(self, state: GraphState) -> GraphState:
        author_name = state["author_name"]
        vietnamese_text, english_text = self.processor.get_translated_info(state["author_info"], author_name)
        response = f"ℹ️ **Thông tin về {author_name}:**\n\n**Tiếng Việt:**\n{vietnamese_text}\n\n**Tiếng Anh:**\n{english_text}"
        return {"response": response}

    def handle_book_recommendation(self, state: GraphState) -> GraphState:
        recommendations = state["recommendations"]
        response = "**📖 Kết quả gợi ý:**\n\n"
        if len(recommendations) == 0:
            response += "Không tìm thấy sách phù hợp với yêu cầu của bạn."
        else:
            for _, row in recommendations.iterrows():
                response += f"- **{row['title']}** - {row['author']}\n  🏷️ *Thể loại:* {row['genre']}\n  ⭐ *Đánh giá:* {row['rating']}\n  🔗 [Xem sách]({row['link']})\n\n"
        return {"response": response}

    def handle_book_description(self, state: GraphState) -> GraphState:
        book_title = state["book_title"]
        if not book_title:
            return {"response": "Không tìm thấy tiêu đề sách trong yêu cầu."}
        matches = self.df[self.df['title'].str.lower().str.contains(book_title.lower(), na=False)]
        if len(matches) == 0:
            return {"response": f"Không tìm thấy thông tin về sách '{book_title}' trong cơ sở dữ liệu."}
        book = matches.iloc[0]
        description = book['description']
        lang = detect(description) if description else 'en'
        if lang == 'vi':
            vietnamese_desc = description
            english_desc = self.processor.translator_vi_to_en.translate(vietnamese_desc) if vietnamese_desc else "Không thể dịch mô tả sang tiếng Anh."
        else:
            english_desc = description
            vietnamese_desc = self.processor.translator_en_to_vi.translate(english_desc) if english_desc else "Không thể dịch mô tả sang tiếng Việt."
        response = f"📖 **Mô tả sách '{book['title']}':**\n\n**Tiếng Việt:**\n{vietnamese_desc}\n\n**Tiếng Anh:**\n{english_desc}"
        return {"response": response}

    def handle_other_intents(self, state: GraphState) -> GraphState:
        return {"response": "🙇‍♂️ Xin lỗi, tôi chỉ hỗ trợ chào hỏi, tìm sách, tìm thông tin tác giả, hoặc tìm mô tả sách."}

    def invoke(self, state: GraphState):
        return self.workflow.invoke(state)