from langchain_community.tools import DuckDuckGoSearchRun
import time

class AuthorInfoSearcher:
    def __init__(self):
        self.search = DuckDuckGoSearchRun()
        self.cache = {}

    def search(self, author_name: str) -> tuple[str, str]:
        if author_name in self.cache:
            return self.cache[author_name]
        bio_query = f'"{author_name}" Vietnamese author biography life career contributions'
        books_query = f'famous works by "{author_name}"'
        author_info= self._run_search(bio_query)
        self.cache[author_name] = (author_info)
        return author_info

    def _run_search(self, query: str) -> str:
        retry_count, retry_delay = 5, 20
        for attempt in range(retry_count):
            try:
                result = self.search.run(query)
                return result or f"Không tìm thấy thông tin cho '{query}'."
            except Exception as e:
                if attempt < retry_count - 1 and ("timeout" in str(e).lower() or "ratelimit" in str(e).lower()):
                    time.sleep(retry_delay)
                else:
                    return f"Lỗi khi tìm kiếm: {e}"