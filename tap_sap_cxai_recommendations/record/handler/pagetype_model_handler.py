from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer
from datetime import datetime, date



@Singleton
class PageTypeModelHandler(BaseHandler):

    def generate(self, pagetype_id, model_id, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        config = options.get('config')
        domain = config.get('DOMAIN')
        return {
            'domain': domain,
            'pagetype_id': pagetype_id,
            'model_id': model_id
        } 
            