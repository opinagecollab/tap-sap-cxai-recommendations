from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import uuid
import singer
from datetime import datetime, date



@Singleton
class PageTypeHandler(BaseHandler):

    def generate(self, page_type_name, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        config = options.get('config')
        domain = config.get('DOMAIN')
        return {
            'domain': domain,
            'id': page_type_name.strip().lower().replace(' ','_'),
            'name': page_type_name
        } 
            