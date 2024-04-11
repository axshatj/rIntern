from serpapi import GoogleSearch

class SerpApiExtractor:
    def __init__(self, api_key):
        self.api_key = api_key

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
            for org_result in results['organic_results']:
                if 'snippet' in org_result:
                    snippet = org_result.get('snippet')
                    content += f"Snippet: {snippet}\n\n"
                    
        return content
