import requests
import logging
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from config import Config


class CVEFetcher:
    def __init__(self, config: Config):
        self.base_url = config.app_config.api_base_url
        self.cve_api_endpoint = config.app_config.cve_api_endpoint
        self.full_api_url = f"{self.base_url}{self.cve_api_endpoint}"
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
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"macOS\""
        }
        self.max_workers = config.app_config.max_workers

    def fetch_cve_details(self, cve_list: List[str]) -> Dict[str, Optional[Dict]]:
        results: Dict[str, Optional[Dict]] = {}
        found_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor, tqdm(total=len(cve_list)) as progress:
            future_to_cve = {executor.submit(self._fetch_single_cve, cve): cve for cve in cve_list}

            for future in as_completed(future_to_cve):
                cve, result = future.result()
                results[cve] = result
                found_count += 1 if result else 0
                progress.update(1)

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
        params = {"id": cve_id, "project": "Central Console"}
        try:
            response = requests.get(self.full_api_url, headers=self.headers, params=params)
            response.raise_for_status()
            return cve_id, response.json()
        except requests.RequestException as e:
            logging.error(f"Request failed for CVE {cve_id}: {e}")
            return cve_id, None
