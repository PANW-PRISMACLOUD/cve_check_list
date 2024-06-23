import json
import logging
from typing import Any, List, Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JSONFileHandler:
    """
    Class to handle JSON file operations.
    """

    def __init__(self, filename: str):
        """
        Initialize the JSONFileHandler with the specified filename.
        
        Args:
            filename (str): Path to the JSON file.
        """
        self.filename = filename

    def load(self) -> Optional[Dict[str, Any]]:
        """
        Load data from a JSON file.
        
        Returns:
            Optional[Dict[str, Any]]: Parsed JSON data as a dictionary or None if an error occurs.
        """
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {self.filename}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error in {self.filename}: {e}")
        return None

    def save(self, data: Dict[str, Any]):
        """
        Save data to a JSON file.
        
        Args:
            data (Dict[str, Any]): Data to be saved.
        """
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            logging.info(f"Data saved to {self.filename}")
        except IOError as e:
            logging.error(f"Error writing to file {self.filename}: {e}")

def load_cve_list(filename: str) -> List[str]:
    """
    Load CVE list from a specified file.
    
    Args:
        filename (str): Path to the file containing the CVE list.
    
    Returns:
        List[str]: A list of CVEs or an empty list if the file cannot be processed.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("cves", [])
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in {filename}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading {filename}: {e}")
    return []

def save_cve_details(filename: str, cve_details: Dict[str, Any]):
    """
    Save CVE details to a specified file.
    
    Args:
        filename (str): Path to the file where the CVE details will be saved.
        cve_details (Dict[str, Any]): CVE details to be saved.
    """
    handler = JSONFileHandler(filename)
    handler.save(cve_details)
