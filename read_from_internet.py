from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
load_dotenv()
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
class SerpApiExtractor:
    def __init__(self, api_key):
        self.api_key = serpapi_api_key

    def extract_content(self, query):
        content = ""
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if 'organic_results' in results:
            for result in results['organic_results']:
                title = result.get('title')
                snippet = result.get('snippet')
                link = result.get('link')
                content += f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n\n"
        return content

