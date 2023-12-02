import requests
from bs4 import BeautifulSoup
import re
import json

def get_function_schema():
    return {
        "name": "web_content_scraper",
        "description": "Scrapes a given URL using Beautiful Soup library, strips out HTML tags, and only reads the content inside the header (h1, h2, etc.) and paragraph (p) tags. Returns the stripped content.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL of the webpage to scrape"
                }
            },
            "required": ["url"]
        }
    }

def handle_response(arguments):
    arguments = json.loads(arguments)
    url = arguments["url"]

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract header and paragraph tags
        header_tags = soup.find_all(re.compile(r"^h\d$"))
        paragraph_tags = soup.find_all("p")

        # Strip HTML tags and collect text content
        stripped_content = ""
        for tag in header_tags + paragraph_tags:
            stripped_content += " " + tag.get_text()

        return stripped_content.strip()
    except Exception as e:
        return f"Error scraping URL '{url}': {str(e)}"
