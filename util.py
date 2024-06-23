import os
import json
from typing import Optional, Type, TypeVar
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

T = TypeVar('T')

def load_json_file(filename: str) -> Optional[T]:
    """
    Load data from a JSON file.
    
    Args:
        filename (str): Path to the JSON file.
    
    Returns:
        Optional[T]: Parsed JSON data or None if an error occurs.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading configuration from {filename}: {e}")
        return None

def get_env_variable(key: str, default: T, type_func: Type[T] = str) -> T:
    """
    Get an environment variable, convert it to a specified type, and provide a default if not found.
    
    Args:
        key (str): Environment variable key.
        default (T): Default value if the environment variable is not found.
        type_func (Type[T]): Function to convert the environment variable to the specified type.
    
    Returns:
        T: Environment variable value converted to the specified type, or the default value.
    """
    try:
        value = os.getenv(key.lower())
        if value is not None:
            return type_func(value)
        return default
    except ValueError as e:
        logging.warning(f"Environment variable {key} conversion error: {e}, using default value.")
        return default
