import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

def create_embedding(text):
    embedding_model = 'text-embedding-3-large'
    embedding = openai.Embedding.create(input = [text], model=embedding_model)['data'][0]['embedding']
    return embedding
