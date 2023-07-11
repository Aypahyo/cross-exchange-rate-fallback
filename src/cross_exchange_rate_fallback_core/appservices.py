import importlib


class AppServices:
    def __init__(self) -> None:
        self.yahoo_client = None
        self.tradegate_client = None
        self.converter = None
        self.config = None

    def initialize_service(self, service_name : str, class_ : type):
        if not isinstance(service_name, str):
            raise TypeError(f"service_name must be str, not {type(service_name)}")
        if not isinstance(class_, type):
            raise TypeError(f"class_ must be type, not {type(class_)}")
        if not hasattr(self, service_name):
            raise ValueError(f"Unknown service: {service_name}")
        setattr(self, service_name, class_(self))

