from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer
from datetime import datetime, date



@Singleton
class RecommendationHandler(BaseHandler):

    def generate(self, recommendation, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        LOGGER.info('recommendation',recommendation)
        return {
            'tenant_id': options.get('tenant_id'),
            'user_id': recommendation.get('user_id'),
            'sku': recommendation.get('item_id'),
            'model': options.get('model_id'),
            'model_confidence': recommendation.get('model_confidence'),
            'id': recommendation.get('id'),
            'created_date': recommendation.get('created_date'),
            #TODO: change to modified date when API passes that in future
            'modified_date': recommendation.get('created_date'),
            'context': recommendation.get('context'),
            'recommendation_id': recommendation.get('user_id')+'|'+recommendation.get('item_id')+'|'+recommendation.get('model'),
            'insert_update_flag': '1'
        } 
            