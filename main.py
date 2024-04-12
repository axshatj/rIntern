import os
import openai
from serpapi import GoogleSearch
from dotenv import load_dotenv
from Indexer import Indexer
from pymilvus import MilvusClient
from search import SearchEngine
from common_helper import create_embedding
load_dotenv()
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
openai.api_key = os.environ.get("OPENAI_API_KEY")
bucket_name = os.environ.get("BUCKET_NAME")
folder_prefix = os.environ.get("FOLDER_NAME")
milvus_collection_name =  os.environ.get("MILVUS_COLLECTION_NAME")

milvus_client = MilvusClient(
    uri=os.getenv("MILVUS_ENDPOINT"),
    token=os.getenv("MILVUS_API_KEY")
)

# connect to milvus
# indexer = Indexer(milvus_client, milvus_collection_name)



# get text from pdf and insert at the same time just comment out the insert portion

# indexer.get_pdf_content(bucket_name, folder_prefix)




# insert knowledge base in the database

# indexer.text_to_vectordb("knowledge base")



# search over the embeddings and internet

# searchengine = SearchEngine(milvus_client, milvus_collection_name, serpapi_api_key)
# print(searchengine.search("who is the founder of google))
