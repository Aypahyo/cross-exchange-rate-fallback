import unittest

import pandas
from cross_exchange_rate_fallback_core.config import Config
from cross_exchange_rate_fallback_core.yahooclient import YahooClient
from cross_exchange_rate_fallback_core.appservices import AppServices

class StockClientTest(unittest.TestCase):

    def setUp(self) -> None:
        self.services = AppServices()
        self.services.initialize_service("config", Config)
        self.sut = YahooClient(self.services)
        return super().setUp()
    
    def test_get_stock_data(self):

        def looks_like_stock_data(input):
            if isinstance(input, pandas.core.frame.DataFrame)and  len(input) > 0:
                return True
            return False
        
        def is_empty(input):
            if isinstance(input, pandas.core.frame.DataFrame) and len(input) == 0:
                return True
            return False


        parameter = [
            {"input": "AAPL", "evaluate": looks_like_stock_data, "error": None},
            {"input": "US42309B4023", "evaluate": looks_like_stock_data, "error": None},
            {"input": "", "evaluate": is_empty, "error": None},
            {"input": None, "evaluate": is_empty, "error": None}, #None is converted to ""
            {"input": 123, "evaluate": None, "error": TypeError},
        ]

        for p in parameter:
            input = p["input"]
            evaluate = p["evaluate"]
            evaluate_name = evaluate.__name__ if evaluate else None
            error = p["error"]
            description = f"input: {input}, evaluate: {evaluate_name}, error: {error}"
            with self.subTest(description):
                if error is None:
                    actual = self.sut.get_stock_data(input)
                    if evaluate is not None:
                        self.assertTrue(evaluate(actual), description)
                    else:
                        self.assertTrue(False, "Invalid test case")
                else:
                    with self.assertRaises(error, msg=description):
                        self.sut.get_stock_data(input)

    def test_get_usd_to_eur(self):
        def looks_like_data(input):
            if isinstance(input, pandas.core.frame.DataFrame)and  len(input) > 0:
                return True
            return False

        parameter = [
            {"testcase": "USD", "evaluate": looks_like_data, "error": None},
        ]

        for p in parameter:
            testcase = p["testcase"]
            evaluate = p["evaluate"]
            evaluate_name = evaluate.__name__ if evaluate else None
            error = p["error"]
            description = f"testcase: {testcase}, evaluate: {evaluate_name}, error: {error}"
            with self.subTest(description):
                if error is None:
                    actual = self.sut.get_usd_to_eur()
                    if evaluate is not None:
                        self.assertTrue(evaluate(actual), description)
                    else:
                        self.assertTrue(False, "Invalid test case")
                else:
                    with self.assertRaises(error, msg=description):
                        self.sut.get_usd_to_eur()