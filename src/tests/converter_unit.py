import unittest
from unittest.mock import MagicMock

import pandas
from cross_exchange_rate_fallback_core.appservices import AppServices

from cross_exchange_rate_fallback_core.converter import Converter

class ConverterTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.services = AppServices()
        self.uut = Converter(self.services)
        return super().setUp()
    
    def test_convert(self):
        parameters = [
            (1, "USD", 1, "USD / USD", 1, "USD", None),
            (1, "USD", 1, "EUR / EUR", None, None, ValueError),
            (100, "USD", 0.85, "EUR / USD", 85, "EUR", None),
            (100, "EUR", 2, "USD / EUR", 200, "USD", None),
            (100, "USD", 1.18, "USD / EUR", 84.7457627118644, "EUR", None),
            ("1", "USD", 1, "USD / USD", None, None, TypeError),
            (1, "USD", "1", "USD / USD", None, None, TypeError),
            (1, "USD", 1, "USD / EUR", 1, "EUR", None),
            (1, 2, 1, "USD / EUR", 1, "EUR", TypeError),
            (1, "USD", 1, 2, 1, "EUR", TypeError),
            (None, "USD", 1, "USD / USD", 1, "USD", TypeError),
            (1, None, 1, "USD / USD", 1, "USD", TypeError),
            (1, "USD", None, "USD / USD", 1, "USD", TypeError),
            (1, "USD", 1, None, 1, "USD", TypeError),
            (1, "USD", 2, "USD / EUR", 0.5, "EUR", None),
            (1, "USD", 2, "EUR / USD", 2, "EUR", None),
        ]

        for source_value, source_currency, rate, rate_unit, expected_value, expected_currency, error in parameters:
            with self.subTest():
                p = { 
                    "source_value": source_value, 
                    "source_currency": source_currency, 
                    "rate": rate, 
                    "rate_unit": rate_unit, 
                    "expected_value": expected_value, 
                    "expected_currency": expected_currency, 
                    "error": error } 
                if error is not None:

                    with self.assertRaises(error, msg=str(p)):
                        self.uut.convert(source_value, source_currency, rate, rate_unit)
                else:
                    try:
                        actual, currency = self.uut.convert(source_value, source_currency, rate, rate_unit)
                        message = f"expected: {expected_value} {expected_currency}, actual: {actual} {currency}\n{p}"
                        self.assertEqual(int(expected_value*1000), int(actual*1000), message)
                        self.assertEqual(expected_currency, currency, message)
                    except Exception as e:
                        self.fail(f"Unexpected exception: {e}\n{p}")

    def test_convert_array(self):
        source_euros = [1, 2, 3]
        source_currency = "EUR"
        rates = [5, 7, 11]
        rate_unit = "USD / EUR"
        expected_dollars = [5, 14, 33]
        expected_currency = "USD"
        actual_dollars, actual_currency = self.uut.convert_array(source_euros, source_currency, rates, rate_unit)
        self.assertEqual(expected_dollars, actual_dollars)
        self.assertEqual(expected_currency, actual_currency)