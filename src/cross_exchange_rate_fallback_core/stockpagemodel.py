import pandas
from cross_exchange_rate_fallback_core.appservices import AppServices


class StockPageModel:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services
        self.stock_search_term = ""
        self.yahoo_stock_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        self.tradegate_stock_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        
    def set_stock_search_term(self, input : str):
        if input is None:
            input = ""
        if not isinstance(input, str):
            raise TypeError(f"input must be str, not {type(input)}")
        self.stock_search_term = input
                
    def get_stock_search_term(self) -> str:
        return self.stock_search_term

    def set_yahoo_stock_data(self, input : pandas.core.frame.DataFrame):
        if input is None:
            input = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        if not isinstance(input, pandas.core.frame.DataFrame):
            raise TypeError(f"input must be pandas.core.frame.DataFrame, not {type(input)}")
        self.yahoo_stock_data = input

    def get_yahoo_stock_data(self) -> pandas.core.frame.DataFrame:
        return self.yahoo_stock_data

    def set_tradegate_stock_data(self, input : pandas.core.frame.DataFrame):
        if input is None:
            input = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        if not isinstance(input, pandas.core.frame.DataFrame):
            raise TypeError(f"input must be pandas.core.frame.DataFrame, not {type(input)}")
        self.tradegate_stock_data = input

    def get_tradegate_stock_data(self) -> pandas.core.frame.DataFrame:
        return self.tradegate_stock_data

    def click_update_stock_data(self):
        client_get_stock_data_methods = [
            lambda x: self.set_yahoo_stock_data(self.app_services.yahoo_client.get_stock_data(x)),
            lambda x: self.set_tradegate_stock_data(self.app_services.tradegate_client.get_stock_data(x)),
        ]

        for client_get_data in client_get_stock_data_methods:
            client_get_data(self.stock_search_term)
        
    def set_field(self, field : str, input):
        if not isinstance(field, str):
            raise TypeError(f"field must be str, not {type(field)}")
        method = f'set_{field}'
        if not hasattr(self, method):
            raise ValueError(f"Unknown method: {method}")
        getattr(self, method)(input)

    def get_field(self, field : str):
        if not isinstance(field, str):
            raise TypeError(f"field must be str, not {type(field)}")
        method = f'get_{field}'
        if not hasattr(self, method):
            raise ValueError(f"Unknown method: {method}")
        return getattr(self, method)()

    def click(self, button : str):
        if not isinstance(button, str):
            raise TypeError(f"button must be str, not {type(button)}")
        method = f'click_{button}'
        if not hasattr(self, method):
            raise ValueError(f"Unknown method: {method}")
        getattr(self, method)()
