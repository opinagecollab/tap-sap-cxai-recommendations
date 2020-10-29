import unittest

from tap_sap_cxai_recommendations.record.factory import build_record_handler
from tap_sap_cxai_recommendations.record.record import Record

from tap_sap_cxai_recommendations.record.handler.recommendation_handler import RecommendationsHandler
from tap_sap_cxai_recommendations.record.handler.product_score_handler import ProductScoresHandler
from tap_sap_cxai_recommendations.record.handler.user_handler import UsersHandler
from tap_sap_cxai_recommendations.record.handler.recommendation_model_handler import RecommendationModelsHandler



class TestFactory(unittest.TestCase):


    def test_should_build_recommendation_handler(self):
        recommendation_handler = build_record_handler(Record.RECOMMENDATIONS)
        self.assertTrue(isinstance(recommendation, RecommendationHandler))

    def test_should_build_scores_handler(self):
        product_score_handler = build_record_handler(Record.SCORES)
        self.assertTrue(isinstance(product_score_handler, ProductScoresHandler))

    def test_should_build_users_handler(self):
        user_handler = build_record_handler(Record.USERS)
        self.assertTrue(isinstance(user_handler, UserHandler))

        def test_should_build_models_handler(self):
        recommendation_model_handler = build_record_handler(Record.RECOMMENDATION_MODELS)
        self.assertTrue(isinstance(recommendation_model_handler, RecommendationModelHandler))
