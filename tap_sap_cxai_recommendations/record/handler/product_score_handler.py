from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import json
import ast
import singer


@Singleton
class ProductScoresHandler(BaseHandler):

    def generate(self, productscores, product_substitution_skus, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        scores = []
        product_substitutions = []
        productscoresarray = ast.literal_eval(productscores)
        for productscore in productscoresarray:
            try:
                score = {
                'tenant_id': options.get('tenant_id'),
                'recommendation_id': options.get('recommendation_id'),
                'sku': productscore['item_id'],
                'score': float(productscore['score']),
                'insert_update_flag': '1'
                }
                scores.append(score)
            except Exception as e:
                LOGGER.error("Invalid product score for recommendation id {}".format(options.get('recommendation_id')))
            # Since product substitutions are part of product score records, fetch them here and only sync if they dont exist already
            substitutions_list = productscore['substitutions']
            for substitution_sku in substitutions_list:
                if not product_substitution_skus or (not substitution_sku in product_substitution_skus):
                    product_substitution = {
                    'tenant_id': options.get('tenant_id'),
                    'sku': productscore['item_id'],
                    'substitute_sku': substitution_sku,
                    'substitution_order': substitutions_list.index(substitution_sku) + 1}
                    product_substitutions.append(product_substitution)
                    product_substitution_skus.append(substitution_sku)
        return (scores, product_substitutions, product_substitution_skus)
        
