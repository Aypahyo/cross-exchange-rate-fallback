import unittest

import pandas
from cross_exchange_rate_fallback_core.config import Config
from cross_exchange_rate_fallback_core.tradegateclient import TradegateClient
from cross_exchange_rate_fallback_core.appservices import AppServices

class TradegateClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.services = AppServices()
        self.services.initialize_service("config", Config)
        self.sut = TradegateClient(self.services)
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
            {"input": "US42309B4023", "evaluate": is_empty, "error": None}, #micromobility.com should be delistet for the hardcoded time period
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

    
    def test_get_ISIN(self):
        parameter = [
            {"input": "AAPL", "expected": "US0378331005"},  # Not an ISIN, too short
            {"input": "US42309B4023", "expected": "US42309B4023"},  # Valid ISIN
            {"input": "", "expected": None},  # Empty string
            {"input": None, "expected": None},  # None
            {"input": 123, "expected": None},  # Not an ISIN, numeric
            {"input": "US-000402625-0", "expected": "US0004026250"},  # Valid ISIN, US company
            {"input": "US0378331009", "expected": None},  # Invalid ISIN
            {"input": "US0378331004", "expected": None},  # Invalid ISIN
            {"input": "US0378331105", "expected": None},  # Invalid ISIN
            {"input": "US0378331005", "expected": "US0378331005"},  # Valid ISIN
            {"input": "US0000000000", "expected": None},  # Not a valid ISIN, lacks unique identifiers
            {"input": "US00000000000", "expected": None},  # Not a valid ISIN, too long
            {"input": "XYZ000000000", "expected": None},  # Not a valid ISIN, invalid country code
            {"input": "US00000O0000", "expected": "US00000O0000"},  # Not a valid ISIN, contains letter O
            {"input": "US000000000I", "expected": None},  # Not a valid ISIN, contains letter I
        ]

        for p in parameter:
            input = p["input"]
            expected = p["expected"]
            description = f"input: {input}, expected: {expected}"
            with self.subTest(description):
                actual = self.sut.getISIN(input)
                self.assertEqual(expected, actual, description)