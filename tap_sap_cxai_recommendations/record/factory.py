from tap_sap_cxai_recommendations.record.record import Record
from tap_sap_cxai_recommendations.record.handler.product_score_handler import ProductScoresHandler
from tap_sap_cxai_recommendations.record.handler.recommendation_handler import RecommendationHandler


def build_record_handler(record: Record):
    if record == Record.SCORES:
        return ProductScoresHandler.get_instance()

    if record == Record.RECOMMENDATIONS:
        return RecommendationHandler.get_instance()

    