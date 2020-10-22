import unittest
import httpretty
import json
import warnings

from tap_sap_cxai_recommendations.client import RecommendationsClient
from tap_sap_cxai_recommendations.resources import recommendation_records, product_scores_list


class TestRecommendationsClient(unittest.TestCase):
    def setUp(self):
        self.client = RecommendationsClient({
            'api_scheme': 'https',
            'api_base_url': 'test:9002',
            'api_base_path': 'api/v1/recommendations/'
        })

        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*")

    def test_should_build_proper_recommendations_url(self):
        self.assertEqual(
            self.client.recommendations_url,
            'https://test:9002/api/v1/recommendations/'
        )


    @httpretty.activate
    def test_should_fetch_recommendations(self):
        # TODO: use multiple pages by splitting list in two
        skip = 0
        httpretty.register_uri(
            httpretty.GET,
            self.client.recommendations_url.format(initial_page),
            body=json.dumps(recommendation_records))

        result = self.client.fetch_recommendations()
        self.assertEqual(recommendation_records, result)
