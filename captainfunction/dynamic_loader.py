# dynamic_loader.py

import os
import importlib
import logging
from types import ModuleType
from typing import Dict, Callable

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def load_modules_from_dir(directory: str) -> Dict[str, ModuleType]:
    """
    Dynamically loads Python modules from a specified directory.

    Args:
    directory (str): The directory to load modules from, relative to this file.

    Returns:
    Dict[str, ModuleType]: A dictionary of module names to module objects.
    """
    modules = {}
    # Get the directory of the current file (__file__ is the path to dynamic_loader.py)
    current_dir = os.path.dirname(__file__)
    full_directory_path = os.path.join(current_dir, directory)

    # Construct the full package path for the functions directory
    package_path = f'captainfunction.{directory}'.replace('/', '.')

    for filename in os.listdir(full_directory_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            try:
                # Use the full package path for importing
                full_module_path = f"{package_path}.{module_name}"
                module = importlib.import_module(full_module_path)
                modules[module_name] = module
                logging.info(f"Successfully loaded module: {module_name}")
            except Exception as e:
                logging.error(f"Error loading module {module_name}: {e}")

    return modules


class FunctionRegistry:
    """
    A registry for dynamically loaded functions.
    """
    def __init__(self):
        self._functions: Dict[str, Callable] = {}

    def register_function(self, name: str, function: Callable):
        """
        Registers a function in the registry.

        Args:
        name (str): The name to register the function under.
        function (Callable): The function to register.
        """
        self._functions[name] = function
        logging.info(f"Function registered: {name}")

    def get_function(self, name: str) -> Callable:
        """
        Retrieves a function from the registry.

        Args:
        name (str): The name of the function to retrieve.

        Returns:
        Callable: The retrieved function.
        """
        return self._functions.get(name, None)

def load_functions(*function_names: str) -> Dict[str, Dict]:
    """
    Loads specified functions and their schemas from the 'functions' directory.

    Args:
    *function_names (str): Names of the modules to load.

    Returns:
    Dict[str, Dict]: A dictionary of module names to their 'handle_response' function callables and schemas.
    """
    loaded_modules = load_modules_from_dir('functions')

    functions = {}
    for module_name, module in loaded_modules.items():
        if hasattr(module, 'handle_response') and hasattr(module, 'get_function_schema'):
            functions[module_name] = {
                'handle_response': module.handle_response,
                'schema': module.get_function_schema()
            }
        else:
            logging.warning(f"Module '{module_name}' does not have the required functions.")

    return functions

