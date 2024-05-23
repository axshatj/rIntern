from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def create_embedding(text):
    embedding_model = 'text-embedding-3-large'
    response = client.embeddings.create(input=[text], model=embedding_model)
    embedding = response.data[0].embedding
    return embedding
