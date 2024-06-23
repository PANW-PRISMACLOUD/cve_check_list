import requests
import logging
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm
from config import Config
import time

class CVEFetcher:
    """
    Class to fetch CVE details using a multi-threaded approach.
    """

    def __init__(self, config: Config):
        """
        Initialize the CVEFetcher with configuration settings.
        """
        self.base_url = config.app_config.api_base_url
        self.cve_api_endpoint = config.app_config.cve_api_endpoint
        self.full_api_url = f"{self.base_url}{self.cve_api_endpoint}"
        self.max_workers = config.app_config.max_workers
        self.session = self._initialize_session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,de;q=0.9",
            "Authorization": f"{config.app_config.auth_key}",
            "Connection": "keep-alive",
            "Dnt": "1",
            "Host": f"{self.base_url.split('//')[0]}",  # Extracts domain from the URL
            "Referer": f"{self.base_url}?jwttoken={config.app_config.jwt_token}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        }

    def _initialize_session(self) -> requests.Session:
        """
        Initialize a requests session with retry logic.
        """
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def fetch_cve_details(self, cve_list: List[str]) -> Dict[str, Optional[Dict]]:
        """
        Fetch details for a list of CVEs using multi-threading.
        
        Args:
            cve_list (List[str]): List of CVE IDs to fetch details for.
        
        Returns:
            Dict[str, Optional[Dict]]: Dictionary containing CVE details and statistics.
        """
        results: Dict[str, Optional[Dict]] = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor, tqdm(total=len(cve_list)) as progress:
            future_to_cve = {executor.submit(self._fetch_single_cve, cve): cve for cve in cve_list}
            for future in as_completed(future_to_cve):
                cve, result = future.result()
                results[cve] = result
                progress.update(1)

        found_count = sum(1 for result in results.values() if result)
        found_percentage = (found_count / len(cve_list)) * 100 if cve_list else 0
        return {
            "results": results,
            "statistics": {
                "total_cves": len(cve_list),
                "found_count": found_count,
                "found_percentage": found_percentage
            }
        }

    def _fetch_single_cve(self, cve_id: str) -> Tuple[str, Optional[Dict]]:
        """
        Fetch details for a single CVE.
        
        Args:
            cve_id (str): CVE ID to fetch details for.
        
        Returns:
            Tuple[str, Optional[Dict]]: Tuple containing CVE ID and its details.
        """
        params = {"id": cve_id, "project": "Central Console"}
        backoff_time = 0.1  # Starting backoff time in seconds

        for attempt in range(3):  # Number of attempts
            try:
                response = self.session.get(self.full_api_url, headers=self.headers, params=params)
                response.raise_for_status()
                return cve_id, response.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    logging.warning(f"Rate limit hit for CVE {cve_id}, retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Exponential backoff
                    continue
                else:
                    logging.error(f"HTTP error for CVE {cve_id}: {e.response.status_code}, {e.response.text}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching CVE {cve_id}: {e}")
            break  # Exit loop if not a 429 error

        return cve_id, None
