import mysql.connector
import pandas as pd
import streamlit as st

class MySQLClient:
    def __init__(self, mysql_config):  # Đổi tên tham số để rõ ràng
        self.config = mysql_config  # Đã là dict chỉ chứa user, password, host, database
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            st.error(f"Lỗi khi kết nối đến MySQL: {str(e)}")

    def load_data(self):
        if not self.conn:
            return pd.DataFrame()
        try:
            query = "SELECT title, author, rating, description, genre, link FROM books"
            df = pd.read_sql(query, self.conn)
            df.fillna("", inplace=True)
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)
            return df
        except Exception as e:
            st.error(f"Lỗi khi tải dữ liệu: {str(e)}")
            return pd.DataFrame()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()