from cross_exchange_rate_fallback_core.appservices import AppServices
from cross_exchange_rate_fallback_core.stockpagemodel import StockPageModel

class AppModel:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services
        self.pagemodels = {
            "stock": StockPageModel(app_services),
        }
    
    def __str__(self):
        return f"AppModel"
    
    def get_pagemodel(self, page : str):
        if not isinstance(page, str):
            raise TypeError(f"page must be str, not {type(page)}")
        if page in self.pagemodels:
            return self.pagemodels[page]
        else:
            raise ValueError(f"Unknown page: {page}")