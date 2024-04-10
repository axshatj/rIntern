import boto3
import openai
import textract
from read_from_s3 import S3PDFExtractor
from read_from_internet import SerpApiExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common_helper import create_embedding
from pymilvus import MilvusClient
from dotenv import load_dotenv
import os


class Indexer:
    MODEL_CHUNK_SIZE = 800

    def __init__(self, milvus_client, milvus_collection_name):
        self.milvus_client = milvus_client
        self.milvus_collection_name = milvus_collection_name
    
    def get_pdf_content(self, bucket_name, folder_prefix):
        extractor = S3PDFExtractor(bucket_name, folder_prefix)
        file_list = extractor.list_pdf_files()
        for pdf_file in file_list:
            pdf_text = extractor.extract_text_from_pdf(pdf_file)
            # print(pdf_text)
            # self.text_to_vectordb(pdf_text) 

    def get_internet_content(self, serpapi_api_key, Query):
        extractor = SerpApiExtractor(serpapi_api_key)
        query = Query
        internet_text = extractor.extract_content(query)
        # print(internet_text)
        # self.text_to_vectordb(internet_text) 

    def text_to_vectordb(self, content):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.MODEL_CHUNK_SIZE,
            chunk_overlap  = self.MODEL_CHUNK_SIZE
        )
        docs = text_splitter.create_documents([content])
        for doc in docs:
            embedding = create_embedding(doc.page_content)
            # self.insert_embedding(embedding)
  
    def insert_embedding(self, embedding):
        row = {
            'vector': embedding
        }
        self.milvus_client.insert(self.milvus_collection_name, data=[row])
