import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pymilvus import MilvusClient
from search import SearchEngine

class MySearchEngine:
    def __init__(self):
        load_dotenv()
        self.serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.bucket_name = os.environ.get("BUCKET_NAME")
        self.folder_prefix = os.environ.get("FOLDER_NAME")
        self.milvus_collection_name = os.environ.get("MILVUS_COLLECTION_NAME")

        self.milvus_client = MilvusClient(
            uri=os.getenv("MILVUS_ENDPOINT"),
            token=os.getenv("MILVUS_API_KEY")
        )

        self.search_engine = SearchEngine(self.milvus_client, self.milvus_collection_name, self.serpapi_api_key)

    def search(self, query):
        return self.search_engine.search(query)

# Example usage:
# search_engine_instance = MySearchEngine()
# print(search_engine_instance.search("who is the founder of Google"))
