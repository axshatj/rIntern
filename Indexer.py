import boto3
import textract
from read_from_s3 import S3PDFExtractor
from read_from_internet import SerpApiExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common_helper import create_embedding
from pymilvus import MilvusClient
from dotenv import load_dotenv
import os
load_dotenv()
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
bucket_name = os.environ.get("BUCKET_NAME")
folder_prefix = os.environ.get("FOLDER_NAME")

class Indexer:
    MODEL_CHUNK_SIZE = 800

    def __init__(self, milvus_client, milvus_collection_name):
        self.milvus_client = milvus_client
        self.milvus_collection_name = milvus_collection_name
    
    def get_pdf_content(self):
        extractor = S3PDFExtractor(bucket_name, folder_prefix)
        file_list = extractor.list_pdf_files()
        for pdf_file in file_list:
            pdf_text = extractor.extract_text_from_pdf(pdf_file)
            print(pdf_text)
            # path = ??
            # self.text_to_vectordb(pdf_text, path) 

    def get_internet_content(self):
        extractor = SerpApiExtractor(serpapi_api_key)
        query = "RASPUTIN"
        internet_text = extractor.extract_content(query)
        print(internet_text)
        # self.text_to_vectordb(internet_text, path) 

    def text_to_vectordb(self, content, path):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.MODEL_CHUNK_SIZE,
            chunk_overlap  = self.MODEL_CHUNK_SIZE
        )
        docs = text_splitter.create_documents([content])
        for doc in docs:
            embedding = create_embedding(doc.page_content)
            print(embedding)
            # self.insert_embedding(embedding, doc.page_content, path)
  
    def insert_embedding(self, embedding, text, path):
        row = {
            'vector': embedding,
            'text': text,
            'path': path
        }
        self.milvus_client.insert(self.milvus_collection_name, data=[row])

indexer = Indexer("milvus_client", "your_collection_name")

# convert test string to embeddings
# indexer.text_to_vectordb("apple orange wood","a")

# retrieve text from pdf on s3
# indexer.read_from_s3(bucket_name,folder_prefix)

# Call the function to get content from the internet and pass the query
# indexer.get_internet_content()