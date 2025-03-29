import pandas as pd
import mysql.connector
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dữ liệu từ file CSV
df = pd.read_csv("crawl_output/goodreads_shelf_books_processed.csv")

# Xử lý dữ liệu bị thiếu
df.fillna("", inplace=True)

# Chuyển rating về kiểu số, nếu không hợp lệ thì đặt giá trị mặc định là 0
def convert_rating(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

df['rating'] = df['rating'].apply(convert_rating)

# Kết nối MySQL
conn = mysql.connector.connect(user='root', password='123456', host='localhost', database='book_db')
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        description TEXT,
        rating FLOAT,
        genre VARCHAR(255),
        link VARCHAR(500) NULL
    )
""")

# Thêm dữ liệu vào MySQL
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO books (title, author, description, rating, genre, link) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row['title'], row['author'], row['description'], row['rating'], row['genres'], row.get('url', None)))

conn.commit()

# Xác định loại truy vấn (title, author, genre, description)
def determine_query_type(query):
    max_similarity = 0
    query_type = "unknown"
    
    for column in ['title', 'author', 'genre', 'description']:
        vectorizer = TfidfVectorizer(stop_words='english')
        combined_text = df[column].astype(str).tolist() + [query]
        tfidf_matrix = vectorizer.fit_transform(combined_text)
        similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).max()
        
        if similarity > max_similarity:
            max_similarity = similarity
            query_type = column
    
    return query_type

# Gộp các đặc trưng cho TF-IDF
df['features'] = df['title'] + " " + df['author'] + " " + df['description'] + " " + df['genres'] + " rating_" + df['rating'].astype(str)

# Tính toán TF-IDF với cột mới
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = vectorizer.fit_transform(df['features'])

# Lưu vectorizer và ma trận TF-IDF
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("tfidf_matrix.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

print("✅ Dữ liệu đã được xử lý và lưu vào MySQL. TF-IDF đã được tính toán.")