import openai

def create_embedding(text):
    embedding_model = 'text-embedding-3-large'
    embedding = openai.Embedding.create(input = [text], model=embedding_model)['data'][0]['embedding']

    return embedding