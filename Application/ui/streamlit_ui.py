import streamlit as st
import uuid
import time

class StreamlitUI:
    def __init__(self, workflow, conversation_manager):
        self.workflow = workflow
        self.conversation_manager = conversation_manager

    def run(self):
        st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")
        st.title("📚 Book Recommendation Chatbot")
        self._render_sidebar()
        self._render_chat()

    def _render_sidebar(self):
        with st.sidebar:
            st.header("📂 Previous Sessions")
            if st.button("➕ New Session"):
                st.session_state.messages = []
                st.session_state.session_id = str(uuid.uuid4())
            
            for session in self.conversation_manager.get_sessions():
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    if st.button(session["title"], key=f"load_{session['id']}"):
                        st.session_state.messages = self.conversation_manager.load(session["id"])
                        st.session_state.session_id = session["id"]
                with col2:
                    if st.button("❌", key=f"delete_{session['id']}"):
                        self.conversation_manager.delete(session["id"])
                        if "session_id" in st.session_state and st.session_state.session_id == session["id"]:
                            st.session_state.messages = []
                            st.session_state.session_id = str(uuid.uuid4())
                        st.rerun()

    def _render_chat(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("Nhập câu hỏi hoặc yêu cầu:"):
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            initial_state = {
                "user_input": user_input,
                "intent": None,
                "author_name": None,
                "book_title": None,
                "recommendations": None,
                "author_info": None,
                "famous_books": None,
                "response": None
            }
            result = self.workflow.invoke(initial_state)

            bot_response = f"🔍 **Ý định:** {result['intent']}\n\n"
            if result["intent"] == "tìm thông tin tác giả":
                bot_response += f"Bạn muốn tìm thông tin về tác giả: **{result['author_name']}**?\nĐang tìm thông tin về {result['author_name']}...\n\n"
            elif result["intent"] == "tìm mô tả sách":
                bot_response += f"Bạn muốn tìm mô tả sách: **{result['book_title']}**?\nĐang tìm thông tin về {result['book_title']}...\n\n"
            if result["response"]:
                bot_response += result["response"]

            with st.chat_message("assistant"):
                st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

            self.conversation_manager.save(st.session_state.session_id, st.session_state.messages)
            time.sleep(1)  # Giả lập thời gian xử lý