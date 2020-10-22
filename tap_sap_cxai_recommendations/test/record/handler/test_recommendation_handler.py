import unittest

from tap_sap_cxai_recommendations.record.factory import build_record_handler
from tap_sap_cxai_recommendations.record.record import Record


class TestRecommendationsHandler(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        cls.input_recommendation_data = {'id': 9169, 'user_id': 'AS378UOMHULXO', 'item_id': '', 'recommendations': "[{'item_id': 'B01EMMJR0A', 'score': '0.40773847699165344'}, {'item_id': 'B000V4T32G', 'score': '0.19173990190029144'}, {'item_id': 'B014QLWSSA', 'score': '0.19039160013198853'}, {'item_id': 'B00RLSCLJM', 'score': '0.1623191237449646'}, {'item_id': 'B005AGO4LU', 'score': '0.15105076134204865'}, {'item_id': 'B01F0VP22O', 'score': '0.12317018210887909'}, {'item_id': 'B000NBIMY2', 'score': '0.0955023244023323'}, {'item_id': 'B0058YEJ5K', 'score': '0.09085488319396973'}, {'item_id': 'B000GHRZN2', 'score': '0.0886092483997345'}, {'item_id': 'B000EE1NNA', 'score': '0.08646310865879059'}]", 'model': 'History_based', 'created_date': '2020-09-30T00:21:34.203425+00:00'}, {'id': 9170, 'user_id': 'A1X1ZJUOWLSFPG', 'item_id': '', 'recommendations': "[{'item_id': 'B01C8EVYU0', 'score': '0.2249741107225418'}, {'item_id': 'B000GHRZN2', 'score': '0.1283612698316574'}, {'item_id': 'B014IBJKNO', 'score': '0.06854508072137833'}, {'item_id': 'B005K04AQU', 'score': '0.024845613166689873'}, {'item_id': 'B0058YEJ5K', 'score': '0.013353003188967705'}, {'item_id': 'B0092UF54A', 'score': '0.009906955994665623'}, {'item_id': 'B001CV4R3C', 'score': '-0.043727703392505646'}, {'item_id': 'B005BY2UP8', 'score': '-0.06597983837127686'}, {'item_id': 'B0046BGWBK', 'score': '-0.07028453797101974'}, {'item_id': 'B009MA34NY', 'score': '-0.07421185076236725'}]", 'model': 'History_based', 'created_date': '2020-09-30T00:21:34.408983+00:00'}
        cls.config = {
          "api_scheme": "https",
          "api_base_url": "localhost:9002",
          "api_base_path": "/rest/v2",
          "tenant_id":"t2"
        }
        cls.model_id = 'mdHashId1'
        cls.tenant_id = 't2'

    def test_should_generate_recommendations_record(self):

        expected_recommendation_record = {'tenant_id': 't2', 'user_id': 'AS378UOMHULXO', 'sku': '', 'model': 'mdHashId1', 'model_confidence': None, 'id': 9169, 'created_date': '2020-09-30T00:21:34.203425+00:00', 'context': None, 'recommendation_id': 'AS378UOMHULXO||History_based', 'insert_update_flag': '1'}
        
        recommendation_record = 
            build_record_handler(Record.RECOMMENDATIONS).generate(self.input_recommendation_data, tenant_id=self.tenant_id, model_id = self.model_id)

        self.assertEqual(recommendation_record, expected_recommendation_record)