from tap_sap_cxai_recommendations.record.handler.base import BaseHandler
from tap_sap_cxai_recommendations.record.handler.decorators import Singleton
import json
import ast
import singer
# import logging

LOGGER = singer.get_logger()


@Singleton
class ProductScoresHandler(BaseHandler):

    def generate(self, productscores, all_product_substitution_skus_map, **options):
        LOGGER = singer.get_logger()
        LOGGER.setLevel(level='DEBUG')
        scores = []
        product_substitutions = []
        try:
            productscoresarray = ast.literal_eval(productscores)
        except Exception as e:
            LOGGER.error("different product score format {}".format(e))
            productscoresarray = productscores
        if not all_product_substitution_skus_map:
            all_product_substitution_skus_map = {}
        for productscore in productscoresarray:
            product = productscore['item_id']
            try:
                score = {
                'tenant_id': options.get('tenant_id'),
                'recommendation_id': options.get('recommendation_id'),
                'sku': product,
                'score': float(productscore['score']),
                'insert_update_flag': '1'
                }
                scores.append(score)
            except Exception as e:
                LOGGER.error("Invalid product score for recommendation id {}".format(options.get('recommendation_id')))
            # Since product substitutions are part of product score records, fetch them here and only sync if they dont exist already
            if 'substitutions' in productscore:
                substitution_products = productscore['substitutions']
                if substitution_products and (not product in all_product_substitution_skus_map):
                        # product_substitution = {
                        # 'tenant_id': options.get('tenant_id'),
                        # 'sku': productscore['item_id'],
                        # 'substitute_sku': substitution_sku,
                        # 'substitution_order': substitutions_list.index(substitution_sku) + 1}
                        # product_substitutions.append(product_substitution)
                        all_product_substitution_skus_map[product] = substitution_products
        return (scores, all_product_substitution_skus_map)
        
