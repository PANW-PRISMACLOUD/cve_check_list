import os
import argparse
import logging
from dotenv import load_dotenv
from util import load_json_file
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Define a Pydantic model for configuration validation
class AppConfig(BaseModel):
    auth_key: str
    jwt_token: str
    api_base_url: str
    cve_api_endpoint: str
    list_file: str
    details_file: str
    max_workers: int


class Config:
    DEFAULT_CONFIG_FILE = "config.json"

    _KEYS = {
        "auth_key": {"id": "AUTHORIZATION_KEY", "desc": "Authorization Key"},
        "jwt_token": {"id": "JWT_TOKEN", "desc": "JWT Token"},
        "api_base_url": {"id": "API_BASE_URL", "desc": "API Base URL"},
        "cve_api_endpoint": {"id": "CVE_API_ENDPOINT", "desc": "CVE API Endpoint"},
        "list_file": {"id": "CVE_LIST_FILE", "desc": "CVE List File"},
        "details_file": {"id": "CVE_DETAILS_FILE", "desc": "CVE Details File"},
        "max_workers": {"id": "MAX_WORKERS", "desc": "Max Workers"},
    }

    def __init__(self):
        try:
            load_dotenv()
            parser = argparse.ArgumentParser(description="CVE Fetcher Configuration")
            for key, info in self._KEYS.items():
                parser.add_argument(f"--{info['id']}", help=info['desc'], default="")

            args = parser.parse_args()
            file_config = load_json_file(Config.DEFAULT_CONFIG_FILE)

            # Prioritize environment variables over CLI arguments and file configuration
            self.config_data = {
                key: os.getenv(info['id'].upper()) or getattr(args, info['id'].upper()) or file_config.get(info['id'].upper(), "")
                for key, info in self._KEYS.items()
            }

            # Validate the loaded configuration using Pydantic
            self.app_config = AppConfig(**self.config_data)  # Validate during initialization

        except Exception as e:
            logging.error(f"Error during configuration initialization: {str(e)}")
            raise