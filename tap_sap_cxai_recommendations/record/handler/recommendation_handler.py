from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer



@Singleton
class RecommendationHandler(BaseHandler):

    def generate(self, recommendation, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        LOGGER.info('recommendation',recommendation)
        return {
            'tenant_id': options.get('tenant_id'),
            #TODO: create a sequence utility to generate these IDs
            #'recommendation_id': uuid.uuid4(),
            'recommendation_id':recommendation.get('id'),
            'user_id': recommendation.get('user_id'),
            'item_id': recommendation.get('item_id'),
            'model': recommendation.get('model'),
            'model_confidence': recommendation.get('model_confidence'),
            'id': recommendation.get('id'),
            'context': recommendation.get('context')
            }