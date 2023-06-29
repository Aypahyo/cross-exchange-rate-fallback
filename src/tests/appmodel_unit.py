import unittest

from cross_exchange_rate_fallback_core.appmodel import AppModel

class AppModelTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.services = None
        self.uut = AppModel(self.services)
        return super().setUp()

    def test_get_pagemodel(self):
        parameter = [
            ("stock", "StockPageModel", None),
            ("unknown", None, ValueError),
            (None, None, TypeError)
        ]

        for page, expected, error in parameter:
            with self.subTest(page=page, expected=expected, error=error):
                if error:
                    with self.assertRaises(error):
                        self.uut.get_pagemodel(page)
                else:
                    actual = self.uut.get_pagemodel(page)
                    self.assertEqual(expected, actual.__class__.__name__)
