import logging
import json
from config import Config
from cve_fetcher import CVEFetcher
from file_utils import load_cve_list, save_cve_details

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():

    # Load configuration
    config = Config()

    # Initialize CVE Fetcher
    cve_fetcher = CVEFetcher(config)

    # Load the list of CVEs to be fetched
    cve_list = load_cve_list(config.app_config.list_file)
    if not cve_list:
        logging.error("No CVEs to fetch. Exiting.")
        return

    # Fetch CVE details
    cve_details = cve_fetcher.fetch_cve_details(cve_list)

    # Save the fetched CVE details
    save_cve_details(config.app_config.details_file, cve_details)

    # Logging the process completion and statistics
    logging.info("CVE fetching process completed.")
    logging.info("Statistics:\n" + json.dumps(cve_details["statistics"], indent=4))


if __name__ == "__main__":
    main()
