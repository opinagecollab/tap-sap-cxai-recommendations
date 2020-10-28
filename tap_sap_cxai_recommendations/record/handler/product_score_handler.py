from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import json
import ast
import singer


@Singleton
class ProductScoresHandler(BaseHandler):

    def generate(self, productscores, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        scores = []
        productscoresarray = ast.literal_eval(productscores)
        for productscore in productscoresarray:
            score = {
            'tenant_id': options.get('tenant_id'),
            'recommendation_id': options.get('recommendation_id'),
            'sku': productscore['item_id'],
            'score': float(productscore['score']),
            'insert_update_flag': '1'
            }
            scores.append(score)
        return scores
        
