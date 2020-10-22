from tap_sap_cxai_recommendations.record.record import Record
from tap_sap_cxai_recommendations.record.handler.product_score_handler import ProductScoresHandler
from tap_sap_cxai_recommendations.record.handler.recommendation_handler import RecommendationHandler
from tap_sap_cxai_recommendations.record.handler.user_handler import UserHandler
from tap_sap_cxai_recommendations.record.handler.recommendation_model_handler import RecommendationModelHandler


def build_record_handler(record: Record):
    if record == Record.SCORES:
        return ProductScoresHandler.get_instance()

    if record == Record.RECOMMENDATIONS:
        return RecommendationHandler.get_instance()

    if record == Record.RECOMMENDATION_MODELS:
        return RecommendationModelHandler.get_instance()

    if record == Record.USERS:
        return UserHandler.get_instance()

    