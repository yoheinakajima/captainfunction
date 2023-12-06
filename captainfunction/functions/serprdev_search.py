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


def format_search_results(results):
    formatted_text = ""
    for item in results['organic']:
        formatted_text += f"{item['position']}. **{item['title']}**\n"
        formatted_text += f"   - **Link**: {item['link']}\n"
        formatted_text += f"   - **Snippet**: \"{item['snippet']}\"\n"
        if 'sitelinks' in item:
            formatted_text += "   - **Sitelinks**:\n"
            for link in item['sitelinks']:
                formatted_text += f"     - [{link['title']}]({link['link']})\n"
        formatted_text += "\n"
    return formatted_text


def handle_response(arguments):
    arguments = json.loads(arguments)
    searchInput = arguments["searchInput"]

    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": searchInput
    })

    headers = {
        'X-API-KEY': os.getenv('SERPRDEV_API_KEY'),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return format_search_results(response.json())
    except requests.exceptions.RequestException as e:
        return f"An error occurred during the search: {str(e)}"
