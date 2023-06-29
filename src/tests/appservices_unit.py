import unittest

from cross_exchange_rate_fallback_core.appservices import AppServices

class FakeStockClient:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services

class CtorErrorService:
    def __init__(self):
        pass


class AppServicesTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.uut = AppServices()
        return super().setUp()
    
    def test_initiaize_yahoo_client(self):

        parameter = [
            {"service_name": "yahoo_client", "class" : FakeStockClient,  "error": None},
            {"service_name": "yahoo_client", "class" : CtorErrorService, "error": TypeError},
            {"service_name": "yahoo_client", "class" : None,             "error": TypeError},
            {"service_name": "unknown",      "class" : FakeStockClient,  "error": ValueError},
            {"service_name": None,           "class" : FakeStockClient,  "error": TypeError},
            {"service_name": 123,            "class" : FakeStockClient,  "error": TypeError},
            {"service_name": "yahoo_client", "class" : 123,             "error": TypeError},
        ]

        for p in parameter:
            service_name = p["service_name"]
            class_ = p["class"]
            error = p["error"]
            description = f"service_name={service_name}, class={class_}, error={error}"
            with self.subTest(service_name=service_name, class_=class_, error=error):
                if error:
                    with self.assertRaises(error, msg=description):
                        self.uut.initialize_service(service_name, class_)
                else:
                    self.uut.initialize_service(service_name, class_)
                    actual = self.uut.__dict__[service_name]
                    self.assertEqual(class_, actual.__class__, msg=description)
