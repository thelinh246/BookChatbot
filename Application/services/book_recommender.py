import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class BookRecommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.vectorizer = None
        self.tfidf_matrix = None
        self.load_tfidf_data()

    def load_tfidf_data(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            vectorizer_path = os.path.join(base_dir, "data", "tfidf_vectorizer.pkl")
            matrix_path = os.path.join(base_dir, "data", "tfidf_matrix.pkl")
            with open(vectorizer_path, "rb") as f:
                self.vectorizer = pickle.load(f)
            with open(matrix_path, "rb") as f:
                self.tfidf_matrix = pickle.load(f)
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file {str(e)}. Vui lòng chạy script tạo file trước.")

    def recommend(self, query: str) -> pd.DataFrame:
        # Kiểm tra None thay vì dùng not trực tiếp
        if self.vectorizer is None or self.tfidf_matrix is None:
            return pd.DataFrame()
        query_vector = self.vectorizer.transform([query.lower()])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        df_copy = self.df.copy()
        df_copy['similarity'] = similarities * (df_copy['rating'] / 5)
        recommendations = df_copy.sort_values(by='similarity', ascending=False).head(5)
        if len(recommendations) == 0 or max(similarities) < 0.1:
            keyword = "science" if "science" in query.lower() else query.lower()
            results = self.df[self.df['genre'].str.lower().str.contains(keyword, na=False) |
                             self.df['title'].str.lower().str.contains(keyword, na=False) |
                             self.df['description'].str.lower().str.contains(keyword, na=False)]
            recommendations = results.sort_values(by='rating', ascending=False).head(5)
        return recommendations