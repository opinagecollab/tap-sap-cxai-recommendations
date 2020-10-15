from urllib.parse import urlunparse

import singer
import requests
import urllib3

LOGGER = singer.get_logger()


class RecommendationsClient:


    def __init__(self, config):
        self.scheme = config['api_scheme']
        self.base_url = config['api_base_url']
        self.base_path = config['api_base_path']

        self.recommendations_url = urlunparse((
            self.scheme, self.base_url, self.base_path , None, None, None
        ))

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_recommendations(self):
        response = requests.get(self.recommendations_url, verify=False, timeout=10)

        if response.status_code != 200:
            raise Exception('Failed to fetch recommendations with status code: {}'.format(response.status_code))

        return response.json()