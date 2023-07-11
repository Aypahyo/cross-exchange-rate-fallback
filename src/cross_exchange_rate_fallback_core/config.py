from cross_exchange_rate_fallback_core.appservices import AppServices


class Config:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services
        self.start = "2023-06-01"
        self.end_inclusve = "2023-06-16"
        self.end_exclusve = "2023-06-17"