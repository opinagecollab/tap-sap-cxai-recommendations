import unittest

from tap_sap_commerce_cloud.record.factory import build_record_handler
from tap_sap_commerce_cloud.record.record import Record

from tap_sap_commerce_cloud.record.handler.category_handler import CategoryHandler
from tap_sap_commerce_cloud.record.handler.customer_specific_price_handler import CustomerSpecificPriceHandler
from tap_sap_commerce_cloud.record.handler.price_point_handler import PricePointHandler
from tap_sap_commerce_cloud.record.handler.product_handler import ProductHandler
from tap_sap_commerce_cloud.record.handler.product_spec_handler import ProductSpecHandler
from tap_sap_commerce_cloud.record.handler.spec_handler import SpecHandler
from tap_sap_commerce_cloud.record.handler.stock_point_handler import StockPointHandler


class TestFactory(unittest.TestCase):


    def test_should_build_recommendation_handler(self):
        recommendation_handler = build_record_handler(Record.RECOMMENDATIONS)
        self.assertTrue(isinstance(recommendation, RecommendationsHandler))

    def test_should_build_scores_handler(self):
        stock_point_handler = build_record_handler(Record.STOCK_POINT)
        self.assertTrue(isinstance(stock_point_handler, StockPointHandler))
