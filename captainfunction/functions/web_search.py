import requests
import os
import json
from metaphor_python import Metaphor

def get_function_schema():
    return {
        "name": "web_search",
        "description": "This function performs a web search using the Metaphor Search API and returns the results.",
        "parameters": {
            "type": "object",
            "properties": {
                "searchInput": {
                    "type": "string",
                    "description": "The input for the search."
                }
            },
            "required": ["searchInput"]
        }
    }

def handle_response(arguments):
    arguments = json.loads(arguments)
    searchInput = arguments["searchInput"]

    metaphor = Metaphor(api_key=os.getenv('METAPHOR_API_KEY'))
  
    try:
        results = metaphor.search(searchInput, use_autoprompt=True)
        print(results)
        return str(results)
    except requests.exceptions.RequestException as e:
        return f"An error occurred during the search: {str(e)}"
