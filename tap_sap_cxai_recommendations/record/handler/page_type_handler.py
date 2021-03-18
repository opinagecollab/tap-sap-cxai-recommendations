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
        return {
            'tenant_id': options.get('tenant_id'),
            'id': page_type_name.strip().lower().replace(' ','_'),
            'name': page_type_name
        } 
            