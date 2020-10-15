from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import json
import ast


@Singleton
class ProductScoresHandler(BaseHandler):

    def generate(self, productscores, **options):
        scores = []
        productscoresarray = ast.literal_eval(productscores)
        for productscore in productscoresarray:
            score = {
            'tenant_id': options.get('tenant_id'),
            'recommendation_id': options.get('recommendation_id'),
            'item_id': productscore['item_id'],
            'score': float(productscore['score']),
            }
        scores.append(score)
        return scores
        
