from src.api_wrapper import SemanticSearchApi

def semantic_search():
    api_key = '/Users/tara/Downloads/nwo-gcp-key.json'
    search = SemanticSearchApi(api_key)

    while True:
        query = input("Query word: ")
        response = search.get_trends(query)
        print(response)

if __name__ == "__main__":
    semantic_search()