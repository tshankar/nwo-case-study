import sys
from src.api_wrapper import SemanticSearchApi

def main(args):
    # try:
    #     query = args[1]
    #     api_key = '/Users/tara/Downloads/nwo-gcp-key.json'
    #     semantic_search = SemanticSearchApi(api_key)
    #     semantic_search.get_trends(query)
    # except: 
    #     print("Must supply exactly one query phrase")


    query = args[1]
    api_key = '/Users/tara/Downloads/nwo-gcp-key.json'
    semantic_search = SemanticSearchApi(api_key)
    semantic_search.get_trends(query)

    print("Must supply exactly one query phrase")
   


if __name__ == "__main__":
    main(sys.argv)