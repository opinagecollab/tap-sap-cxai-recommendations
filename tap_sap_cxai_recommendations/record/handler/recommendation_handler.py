from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer
from datetime import datetime, date

LOGGER = singer.get_logger()
LOGGER.setLevel(level='DEBUG')

@Singleton
class RecommendationHandler(BaseHandler):

    def generate(self, recommendation, **options):
        config = options.get('config')
        data_source = config.get('RECOMMENDATION_SOURCE')
        model_confidence = recommendation.get('model_confidence')
        if recommendation.get('model_confidence') is None:
            model_confidence = 0
        else:
            model_confidence = float(recommendation.get('model_confidence'))
        user_id = recommendation.get('user_id')
        if not user_id:
            user_id = ''
        sku =  recommendation.get('item_id')
        if not sku:
            sku = ''
        model = recommendation.get('model')
        if not model:
            model = ''
        return {
            'tenant_id': options.get('tenant_id'),
            'user_id': user_id,
            'sku': sku,
            'model': model,
            'model_id': options.get('model_id'),
            'model_confidence': model_confidence,
            'id': recommendation.get('id'),
            'created_date': recommendation.get('created_date'),
            #TODO: change to modified date when API passes that in future
            'modified_date': recommendation.get('created_date'),
            'context': recommendation.get('context'),
            'recommendation_id': user_id+'|'+sku+'|'+model,
            'insert_update_flag': '1',
            'source': data_source
        } 
            