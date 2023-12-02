import os
from openai import OpenAI
import importlib
import json

def get_function_schema():
    return {
        "name": "function_saver",
        "description": "Writes and saves new OpenAI functions into the the 'functions' folder, which get automatically loaded. It should be used when a user asks for a function to be written, saved, or a new skill or capability to be created for yourself (the AI assistant).",
        "parameters": {
            "type": "object",
            "properties": {
              "function_description": {
                  "type": "string",
                  "description": "Detailed description of the function to be created, enhanced with purpose, when it should be used, and how it works."
              },
            }
        }
    }

def handle_response(arguments):
    arguments = json.loads(arguments)
    function_description = arguments["function_description"]
    # Function to read and format code from files
    def read_and_format_code(file_name):
        module_name = file_name[:-3]
        module = importlib.import_module(f"functions.{module_name}")
        function_schema = module.get_function_schema()
        with open(os.path.join('functions', file_name), 'r') as file:
            code = file.read()
        return function_schema["description"], code

    # Read example codes and descriptions
    descriptions_and_codes = [read_and_format_code(file) for file in ["list_directory_files.py", "function_saver.py", "read_file_contents.py"]]

    # Construct the conversation messages
    messages = []
    messages.append({"role":"system","content":""" Write a new function based on user input and respond only with the code. This is for the OpenAI function call functionality, where the get_function_schema can be used to define the arguments (if more than one), and be passed to an API and return results. get_function_schema() defines the function call and sets the parameters, which are then sent into handle_response directly to ping an API (or multiple APIs) and run code which returns either data requested or results of a task."""})
    for desc, code in descriptions_and_codes:
        messages.append({"role": "user", "content": f"Function: {desc}"})
        messages.append({"role": "assistant", "content": code})

    # Add the final user message
    messages.append({"role": "user", "content": f"Function: {function_description}"})
    #print(messages)
    # Call OpenAI API with the conversation messages
    client = OpenAI()
    code_extraction = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract and handle the generated code
    generated_code = code_extraction.choices[0].message.content
    print(generated_code)

    # Generate a file name for the new function
    file_name_prompt = f"Generate a file name for the following python function: {generated_code}\n###\nFILE_NAME:"
    file_name_generation = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": file_name_prompt}]
    )
    file_name = file_name_generation.choices[0].message.content.strip()
    file_path = os.path.join('functions', file_name)

    # Save the new function code
    try:
        with open(file_path, 'w') as file:
            file.write(generated_code)
            print(f"Function saved to {file_path}")
            return f"Code saved successfully: {file_name}"
    except Exception as e:
        return f"Error saving code: {e}"
