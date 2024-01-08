import os
import json
from typing import Optional, Type
from typing import TypeVar
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

T = TypeVar('T')


def load_json_file(filename) -> Optional[T]:
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
    """
    try:
        value = os.getenv(key.lower())
        if value is not None:
            return type_func(value)
        return default
    except ValueError as e:
        logging.warning(f"Environment variable {key} conversion error: {e}, using default value.")
        return default