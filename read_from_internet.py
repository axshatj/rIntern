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
            for result in results['organic_results']:
                title = result.get('title')
                snippet = result.get('snippet')
                link = result.get('link')
                content += f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n\n"
        return content

