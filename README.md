# Welcome to CaptainFunction! 🚀

CaptainFunction is a dynamic Python library for loading custom functions into OpenAI's powerful AI models. This toolkit makes integrating custom functionalities into OpenAI Assistants both easy and flexible.

I'm releasing this with two basic functions to start, a web search using Metaphor and a web scrape using BeautifulSoup. Both can be improved, but this way when I improve a function in one place, it improves everywhere I use it. You are more than welcome to contribute!

## Getting Started 🌟

### Prerequisites

- Python 3.6 or later.
- Access to OpenAI's API (API key).
- Other API keys depending on the function you load.

### Installation

1. **Install CaptainFunction:**
   ```
   pip install git+https://github.com/yoheinakajima/captainfunction.git
   ```

*Note, you currently need to separately install required libraries from each function you load.

### Contributing Functions

Contribute your best functions in the `functions` directory. Each function should be in its separate file. The names get_function_schema() and handle_response() should not be changed. For example:
```
import os

def get_function_schema():
    return {
        "name": "function_name",
        "description": "What your function does.",
        "parameters": {
            "type": "object",
            "properties": {
                "argument1": {
                    "type": "string",
                    "description": "The first argument."
                },
                ...
            }
        }
    }

def handle_response(arguments):
    arguments = json.loads(arguments)
    argument1 = arguments["argument1"]
    # Your function logic here
    return "Function response"
```

## Using CaptainFunction 🛠️

### Loading Functions into OpenAI Assistant

First, load your functions using the `load_functions` method. For instance:
```
loaded_funcs = load_functions('web_search','web_content_scraper')
```

This loads the functions 'web_search' and 'web_content_scraper' from the `functions` directory.

### Integrating with OpenAI Assistant

Create the function schemas and initialize the OpenAI assistant (this examples is for Assistants API, need to adjust for other endpoints):
```
function_schemas = [{"type": "function", "function": func['schema']} for func in loaded_funcs.values()]

assistant = openai_client.beta.assistants.create(
    instructions="Respond to user queries.",
    model="gpt-3.5-turbo",
    tools=function_schemas
)
```

### Handling OpenAI API Calls

Handle the function calls in your application logic (this examples is for Assistants API, need to adjust for other endpoints):
```
# Wait for run to complete
while True:
    run_response = openai_client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run_response.status == "completed":
        break
    elif run_response.status == "requires_action":
        # Handle function calls
        tool_outputs = []
        for tool_call in run_response.required_action.submit_tool_outputs.tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            if function_name in loaded_funcs:
                handle_response_func = loaded_funcs[function_name]['handle_response']
                output = handle_response_func(arguments)
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": output,
                })

        openai_client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        pass
    time.sleep(1)  # Avoid spamming the API too quickly
```

## Contributing 🤝

We encourage contributions! Feel free to add new functions or improve existing ones. To contribute:

- Fork the repository.
- Create a new branch for your contribution.
- Add your new function or improvements.
- Submit a pull request.

All contributions are welcome (including helping manage any repo, because I'm candidly not great at it).

## License 📄

MIT
