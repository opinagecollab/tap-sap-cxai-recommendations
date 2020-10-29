from urllib.parse import urlunparse
from tap_sap_cxai_recommendations.record.record import Record

import singer
import requests
import urllib3
import json

LOGGER = singer.get_logger()


class RecommendationsClient:


    def __init__(self, config):
        self.scheme = config['api_scheme']
        self.base_url = config['api_base_url']
        self.base_path = config['api_base_path']
        self.param_skip = config['param_skip']
        self.param_take = config['param_take']
        self.url_count_suffix = '/total_count'
        self.total_count_label = 'total_records'

        self.recommendations_url = urlunparse((
            self.scheme, self.base_url, self.base_path , None, None, None
        ))

        self.recommendations_url_count = urlunparse((
            self.scheme, self.base_url, self.base_path+self.url_count_suffix , None, None, None
        ))

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_recommendations(self, state, bookmark_column):
        LOGGER.info('parameters')
        LOGGER.info(self.param_take)

        # Get total number of recommendation records
        response_count = requests.get(self.recommendations_url_count, verify=False, timeout=10)
        LOGGER.info('recommendations total count json')
        LOGGER.info(response_count)
        json_response_count = response_count.json()
        LOGGER.info(json_response_count)
        recommendation_count = json_response_count[self.total_count_label]
        LOGGER.info(recommendation_count)

        try:
            iteration_count = int(recommendation_count/int(self.param_take))
        except ValueError:
            LOGGER.error('invalid take parameter', self.param_take)

        LOGGER.info('iteration count')
        LOGGER.info(iteration_count)

        skip = 0
        resp_temp = ''
        for x in range(0, iteration_count+1):
            response_loop = requests.get(self.recommendations_url, params = {"skip": skip, "take":self.param_take}, verify=False, timeout=10)
            if response_loop.status_code != 200:
                raise Exception('Failed to fetch recommendations with status code: {}'.format(response_loop.status_code))
            LOGGER.info('count value: %d',x)
            # LOGGER.info(response_loop.json())
            response_str = json.dumps(response_loop.json())
            if not resp_temp:
                resp_temp = response_str[1:len(response_str)-1]
            else:
                resp_temp = resp_temp+','+response_str[1:len(response_str)-1]
            skip = skip + int(self.param_take)


        json_response = json.loads('['+resp_temp+']')

        
        LOGGER.info(state)
        LOGGER.info(bookmark_column)
        
        last_bookmark = singer.get_bookmark(state, Record.RECOMMENDATIONS.value, bookmark_column)
        LOGGER.info(last_bookmark)

        if last_bookmark is not None:
            json_response_filtered = filter(lambda res: res['created_date'] > last_bookmark, json_response)
            LOGGER.info('Filtered recommendations response')
            LOGGER.info(json_response_filtered)
            json_response = json_response_filtered
        else:
            LOGGER.info('bookmark value not found')

        
        return json_response