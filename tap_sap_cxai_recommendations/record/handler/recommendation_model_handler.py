from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer
from datetime import datetime, date
import hashlib



@Singleton
class RecommendationModelHandler(BaseHandler):

    def generate(self, model_name, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        LOGGER.info(hashlib.md5(model_name.strip().encode('utf-8')).hexdigest())
        return {
            'tenant_id': options.get('tenant_id'),
            'id': hashlib.md5(model_name.strip().encode('utf-8')).hexdigest(),
            'name': model_name
        } 
            