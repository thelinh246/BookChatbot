# Book Recommendation Chatbot

Book Recommendation Chatbot là một ứng dụng chatbot được xây dựng bằng Streamlit, kết hợp với MySQL, Redis, và mô hình TF-IDF để cung cấp gợi ý sách, thông tin tác giả và quản lý lịch sử hội thoại. Dự án được thiết kế theo nguyên tắc SOLID, đảm bảo tính mô-đun và dễ bảo trì.

## 🚀 Tính năng
- **📚 Gợi ý sách:** Nhập từ khóa hoặc câu hỏi để nhận danh sách sách gợi ý dựa trên TF-IDF.
- **👤 Thông tin tác giả:** Tìm kiếm tiểu sử và tác phẩm nổi bật của tác giả thông qua DuckDuckGo.
- **🌍 Dịch song ngữ:** Hiển thị thông tin bằng cả tiếng Việt và tiếng Anh.
- **💾 Quản lý hội thoại:** Lưu trữ và tải lại lịch sử trò chuyện bằng Redis.
- **🖥️ Giao diện thân thiện:** Sử dụng Streamlit để cung cấp giao diện chat trực quan và dễ sử dụng.

## 🛠 Yêu cầu hệ thống
- **Python:** 3.12 hoặc cao hơn (khuyến nghị 3.12.5)
- **MySQL:** Server MySQL chạy cục bộ hoặc từ xa với bảng `books`
- **Redis:** Server Redis để lưu trữ phiên hội thoại
- **API Key:** Khóa API của OpenAI để phân loại ý định người dùng

## 🔧 Cài đặt
### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/book_chatbot.git
cd book_chatbot
cd Application
```
### 2️⃣ Tạo môi trường ảo
```bash
python -m venv venv
```
- **Windows:** `venv\Scripts\activate`
- **Linux/Mac:** `source venv/bin/activate`

### 3️⃣ Cài đặt thư viện
```bash
pip install -r requirements.txt
```
### 4️⃣ Cấu hình biến môi trường
Tạo file `.env` trong thư mục gốc (`book_chatbot/`) với nội dung:
```ini
OPENAI_API_KEY="xxxxxx"
REDIS_HOST=abc
REDIS_PORT=123
REDIS_PASSWORD=abc
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="xxx"
LANGSMITH_PROJECT="xxx"
```

### 5️⃣ Thiết lập cơ sở dữ liệu MySQL
#### Tạo database `book_db`
```sql
CREATE DATABASE book_db;
```
#### Tạo bảng `books`
```sql
USE book_db;
CREATE TABLE books (
    title VARCHAR(255),
    author VARCHAR(255),
    rating FLOAT,
    description TEXT,
    genre VARCHAR(100),
    link VARCHAR(255)
);
```
> 📌 **Thêm dữ liệu mẫu vào bảng `books` trước khi chạy ứng dụng.**

### 6️⃣ Chuẩn bị file TF-IDF
Đặt file `tfidf_vectorizer.pkl` và `tfidf_matrix.pkl` vào thư mục `data/`.
Nếu chưa có, chạy script tạo file (xem phần "Tạo file TF-IDF" bên dưới).

## ▶️ Chạy ứng dụng
```bash
streamlit run app.py
```

## 📌 Tạo file TF-IDF và thêm dữ liệu vào MySQL
Nếu chưa có `tfidf_vectorizer.pkl` và `tfidf_matrix.pkl`, chạy file `process.py` trong thư mục `DataProcess`.
```bash
python DataProcess/process.py
```

## 💡 Hướng dẫn sử dụng
1. **Mở ứng dụng** trong trình duyệt.
2. **Nhập câu hỏi hoặc yêu cầu:**
   - 📖 *"Gợi ý sách về khoa học"* → Gợi ý sách.
   - 👨‍🏫 *"Thông tin về tác giả Stephen Hawking"* → Tiểu sử và tác phẩm nổi bật.
   - 🖐️ *"Xin chào"* → Phản hồi chào hỏi.
3. **Xem lịch sử hội thoại** ở thanh bên trái.
