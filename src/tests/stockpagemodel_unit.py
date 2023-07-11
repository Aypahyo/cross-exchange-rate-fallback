import unittest
from unittest.mock import MagicMock

import pandas

from cross_exchange_rate_fallback_core.stockpagemodel import StockPageModel
from cross_exchange_rate_fallback_core.appservices import AppServices

class StockPageModelTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.services = AppServices()
        self.uut = StockPageModel(self.services)
        return super().setUp()
    
    def test_stock_search_term(self):
        parameter = [
            {"input": "AAPL", "expected": "AAPL", "error": None},
            {"input": "US42309B4023", "expected": "US42309B4023", "error": None},
            {"input": "", "expected": "", "error": None},
            {"input": None, "expected": "", "error": None},
            {"input": 123, "expected": None, "error": TypeError},
        ]

        for p in parameter:
            input = p["input"]
            expected = p["expected"]
            error = p["error"]
            with self.subTest(input=input, expected=expected, error=error):
                if error:
                    with self.assertRaises(error):
                        self.uut.set_stock_search_term(input)
                else:
                    self.uut.set_stock_search_term(input)
                    actual = self.uut.get_stock_search_term()
                    self.assertEqual(expected, actual)

    def test_stock_data(self):
        valid_stock_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], data=[["1", "2", "3", "4", "5", "6"]])
        empty_stock_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

        parameter = [
            {"input": empty_stock_data, "expected": empty_stock_data, "error": None},
            {"input": valid_stock_data, "expected": valid_stock_data, "error": None},
            {"input": None, "expected": empty_stock_data, "error": None},
            {"input": 123, "expected": None, "error": TypeError},
        ]

        for p in parameter:
            input = p["input"]
            expected = p["expected"]
            error = p["error"]
            with self.subTest(input=input, expected=expected, error=error):
                if error:
                    with self.assertRaises(error):
                        self.uut.set_yahoo_stock_data(input)
                else:
                    self.uut.set_yahoo_stock_data(input)
                    actual = self.uut.get_yahoo_stock_data()
                    self.assertEqual(str(expected), str(actual))

    def test_set_get_field(self):
        parameter = [
            {"field" : "stock_search_term", "input": "AAPL", "expected": "AAPL", "error": None},
            {"field" : "stock_search_term", "input": "US42309B4023", "expected": "US42309B4023", "error": None},
            {"field" : "stock_search_term", "input": "", "expected": "", "error": None},
            {"field" : "stock_search_term", "input": None, "expected": "", "error": None},
            {"field" : "stock_search_term", "input": 123, "expected": None, "error": TypeError},
            {"field" : "unknown", "input": "AAPL", "expected": None, "error": ValueError},
            {"field" : None, "input": "AAPL", "expected": None, "error": TypeError},
        ]

        for p in parameter:
            input = p["input"]
            expected = p["expected"]
            error = p["error"]
            field = p["field"]
            with self.subTest(input=input, expected=expected, error=error):
                if error:
                    with self.assertRaises(error):
                        self.uut.set_field(field, input)
                else:
                    self.uut.set_field(field, input)
                    actual = self.uut.get_field(field)
                    self.assertEqual(expected, actual)
    
    def test_click_update_stock_data(self):
        old_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        new_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], data=[["1", "2", "3", "4", "5", "6"]])
        self.services.yahoo_client = MagicMock()
        self.services.yahoo_client.get_stock_data = MagicMock(return_value=new_data)
        self.uut.set_yahoo_stock_data(old_data)
        self.uut.click_update_stock_data()
        actual = self.uut.get_yahoo_stock_data()
        #comparing dataframes is not trivial, so we compare the string representation
        self.assertEqual(str(new_data), str(actual))
    
    def test_click_button(self):
        old_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        new_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], data=[["1", "2", "3", "4", "5", "6"]])
        self.services.yahoo_client = MagicMock()
        self.services.yahoo_client.get_stock_data = MagicMock(return_value=new_data)

        parameter = [
            {"button" : "update_stock_data", "expected": new_data, "error": None},
            {"button" : "unknown", "expected": old_data, "error": ValueError},
            {"button" : None, "expected": old_data, "error": TypeError},
            {"button" : 123, "expected": old_data, "error": TypeError},
        ]

        for p in parameter:
            expected = p["expected"]
            error = p["error"]
            button = p["button"]
            description = f"button={button}, expected={expected}, error={error}"
            self.uut.set_yahoo_stock_data(old_data)
            with self.subTest(expected=expected, error=error):
                if error:
                    with self.assertRaises(error, msg=description):
                        self.uut.click(button)
                else:
                    self.uut.click(button)
                actual = self.uut.get_yahoo_stock_data()
                #comparing dataframes is not trivial, so we compare the string representation
                self.assertEqual(str(expected), str(actual))