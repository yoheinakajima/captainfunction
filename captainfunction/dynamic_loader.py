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
    directory (str): The directory to load modules from.

    Returns:
    Dict[str, ModuleType]: A dictionary of module names to module objects.
    """
    modules = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"{directory}.{module_name}")
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

def load_functions(*function_names: str) -> Dict[str, Callable]:
    """
    Loads specified functions from the 'functions' directory.

    Args:
    *function_names (str): Names of the functions to load.

    Returns:
    Dict[str, Callable]: A dictionary of function names to function callables.
    """
    function_registry = FunctionRegistry()
    loaded_modules = load_modules_from_dir('functions')

    for function_name in function_names:
        for module_name, module in loaded_modules.items():
            if hasattr(module, function_name):
                function_registry.register_function(function_name, getattr(module, function_name))
                break
        else:
            logging.warning(f"Function '{function_name}' not found in any module.")

    return {name: function_registry.get_function(name) for name in function_names}

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     loaded_funcs = load_functions('function1', 'function2')
#     for name, func in loaded_funcs.items():
#         if func:
#             print(f"Running {name}:")
#             result = func()
#             print(f"Result: {result}")
