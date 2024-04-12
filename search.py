from common_helper import create_embedding
from read_from_internet import SerpApiExtractor
import openai

class SearchEngine:
    def __init__(self, milvus_client, milvus_collection_name, serpapi_api_key):
       self.milvus_client = milvus_client
       self.milvus_collection_name = milvus_collection_name
       self.serpapi_api_key = serpapi_api_key

    def query_milvus_and_internet(self, user_query, embedding):
        result_count = 3
        extractor = SerpApiExtractor(self.serpapi_api_key)

        result = self.milvus_client.search(
            collection_name=self.milvus_collection_name,
            data=[embedding],
            limit=result_count,
            output_fields=["text"])

        list_of_knowledge_base = list(map(lambda match: match['entity']['text'], result[0]))
        list_of_knowledge_base_from_internet = extractor.extract_content(user_query)
        list_of_knowledge_base.append(list_of_knowledge_base_from_internet)

        # print(list_of_knowledge_base)
        return {
            'list_of_knowledge_base': list_of_knowledge_base
        }
  
    def query_vector_db(self, user_query, embedding):
        return self.query_milvus_and_internet(user_query, embedding)
  
    def ask_chatgpt(self, knowledge_base, user_query):
        system_content = """You are a Question Answering bot designed to assist users with their queries based on the provided Knowledge Base. 
                            Use the Knowledge Base in the most efficient way to accurately answer the user's questions.
                            If you do not have the answer to a question within the scope of the Knowledge Base, clearly state that you do not know the answer.
                            You will only answer questions related to the content of the Knowledge Base. For any questions outside the Knowledge Base,
                            inform the user that it is beyond your responsibilities.
                            Strictly use only the information contained in the Knowledge Base to formulate your responses. Do not bring in any external data or information.
                            Provide concise answers to simple questions, and more detailed responses for complex or open-ended queries. 
                            Use markdown formatting for any code or technical content in your answers.
                            Do not mention any details about yourself or your capabilities unless they are directly relevant to the user's query.
                        """
  
        user_content = f"""
            Knowledge Base:
            ---
            {knowledge_base}
            ---
            User Query: {user_query}
            Answer:
        """
        system_message = {"role": "system", "content": system_content}
        user_message = {"role": "user", "content": user_content}
        
        chatgpt_response = openai.ChatCompletion.create(model="gpt-4-turbo-2024-04-09", messages=[system_message, user_message])
        return chatgpt_response.choices[0].message.content
  
    def search(self, user_query):
        embedding = create_embedding(user_query)
        result = self.query_vector_db(user_query, embedding)
  
        knowledge_base = "\n".join(result['list_of_knowledge_base'])
        response = self.ask_chatgpt(knowledge_base, user_query)
  
        return {
            'response': response
        }

