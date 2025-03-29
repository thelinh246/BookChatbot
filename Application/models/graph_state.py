from typing import TypedDict
import pandas as pd

class GraphState(TypedDict):
    user_input: str
    intent: str
    author_name: str
    book_title: str
    recommendations: pd.DataFrame
    author_info: str
    famous_books: str
    response: str