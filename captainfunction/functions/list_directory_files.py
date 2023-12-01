import os

def get_function_schema():
    return {
        "name": "list_directory_files",
        "description": "Outputs the file and folder structure of the top parent folder.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }

def handle_response(arguments):
    # Function to get the top parent path
    def get_top_parent_path(current_path):
        while True:
            new_path = os.path.dirname(current_path)
            if new_path == '/home/runner/BabyGhostAPI-1':  # Adjust this to your specific path
                return new_path
            current_path = new_path

    # Function to get directory structure
    def get_directory_structure(start_path):
        dir_structure = {}
        ignore_dirs = ['.', '__pycache__', 'venv']  # Exclude specific directories

        for root, dirs, files in os.walk(start_path):
            dirs[:] = [d for d in dirs if not any(d.startswith(i) for i in ignore_dirs)]
            files = [f for f in files if not f.startswith('.')]  # Exclude hidden files

            current_dict = dir_structure
            path_parts = os.path.relpath(root, start_path).split(os.sep)
            for part in path_parts:
                if part:
                    if part not in current_dict:
                        current_dict[part] = {}
                    current_dict = current_dict[part]
            for f in files:
                current_dict[f] = None
        return dir_structure

    # Get the current script path
    current_script_path = os.path.realpath(__file__)

    # Get the top parent directory and directory structure
    top_parent_path = get_top_parent_path(current_script_path)
    dir_structure = get_directory_structure(top_parent_path)

    return str(dir_structure)
