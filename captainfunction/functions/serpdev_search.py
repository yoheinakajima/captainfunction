import requests
import os
import json


def get_function_schema():
    return {
        "name": "serpdev_search",
        "description": "This function performs a google search using SerpDev and returns the results.",
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

    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": searchInput
    })

    headers = {
        'X-API-KEY': os.getenv('SERPDEV_API_KEY'),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"An error occurred during the search: {str(e)}"
