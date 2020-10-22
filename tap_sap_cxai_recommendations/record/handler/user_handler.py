from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer
from datetime import datetime, date



@Singleton
class UserHandler(BaseHandler):

    def generate(self, user_id, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        LOGGER.info('user',user_id)
        return {
            'tenant_id': options.get('tenant_id'),
            'id': user_id,
            # since we dont know the name, populate id itself as name for now
            'name': user_id
        } 
            