from urllib.parse import urlunparse
from tap_sap_cxai_recommendations.record.record import Record

import singer
import requests
import urllib3

LOGGER = singer.get_logger()


class RecommendationsClient:


    def __init__(self, config):
        self.scheme = config['api_scheme']
        self.base_url = config['api_base_url']
        self.base_path = config['api_base_path']
        self.param_skip = config['param_skip']
        self.param_take = config['param_take']

        self.recommendations_url = urlunparse((
            self.scheme, self.base_url, self.base_path , None, None, None
        ))

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_recommendations(self, state, bookmark_column):
        LOGGER.info('parameters')
        LOGGER.info(self.param_skip)
        LOGGER.info(self.param_take)
        response = requests.get(self.recommendations_url, params = {"skip": self.param_skip, "take":self.param_take}, verify=False, timeout=10)

        if response.status_code != 200:
            raise Exception('Failed to fetch recommendations with status code: {}'.format(response.status_code))

        json_response = response.json()
        LOGGER.info('recommendations response')
        LOGGER.info(json_response)

        
        LOGGER.info(state)
        LOGGER.info(bookmark_column)
        
        last_bookmark = singer.get_bookmark(state, Record.RECOMMENDATIONS.value, bookmark_column)
        LOGGER.info(last_bookmark)
        # try:
        if last_bookmark is not None:
            json_response_filtered = filter(lambda res: res['created_date'] > last_bookmark, json_response)
            LOGGER.info('Filtered recommendations response')
            LOGGER.info(json_response_filtered)
            json_response = json_response_filtered
        else:
            LOGGER.info('bookmark value not found')
        # except NameError:
        #     LOGGER.info('no bookmark in state file')
        
        return json_response