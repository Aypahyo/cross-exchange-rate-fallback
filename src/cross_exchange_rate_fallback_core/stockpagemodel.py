import pandas
from cross_exchange_rate_fallback_core.appservices import AppServices
from cross_exchange_rate_fallback_core.converter import Converter


class StockPageModel:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services
        self.stock_search_term = ""
        self.yahoo_stock_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        self.tradegate_stock_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        self.usd_to_eur = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        self.yahoo_converted_data = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        
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

    def set_yahoo_converted_data(self, input : pandas.core.frame.DataFrame):
        if input is None:
            input = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        if not isinstance(input, pandas.core.frame.DataFrame):
            raise TypeError(f"input must be pandas.core.frame.DataFrame, not {type(input)}")
        self.yahoo_converted_data = input

    def get_yahoo_converted_data(self) -> pandas.core.frame.DataFrame:
        return self.yahoo_converted_data

    def set_tradegate_stock_data(self, input : pandas.core.frame.DataFrame):
        if input is None:
            input = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        if not isinstance(input, pandas.core.frame.DataFrame):
            raise TypeError(f"input must be pandas.core.frame.DataFrame, not {type(input)}")
        self.tradegate_stock_data = input

    def get_tradegate_stock_data(self) -> pandas.core.frame.DataFrame:
        return self.tradegate_stock_data

    def set_usd_to_eur(self, input : pandas.core.frame.DataFrame):
        if input is None:
            input = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        if not isinstance(input, pandas.core.frame.DataFrame):
            raise TypeError(f"input must be pandas.core.frame.DataFrame, not {type(input)}")
        self.usd_to_eur = input
    
    def get_usd_to_eur(self) -> pandas.core.frame.DataFrame:
        return self.usd_to_eur

    def click_update_stock_data(self):
        client_get_stock_data_methods = [
            lambda x: self.set_yahoo_stock_data(self.app_services.yahoo_client.get_stock_data(x)),
            lambda x: self.set_tradegate_stock_data(self.app_services.tradegate_client.get_stock_data(x)),
        ]

        for client_get_data in client_get_stock_data_methods:
            client_get_data(self.stock_search_term)
    
    def click_update_exchange_rate_data(self):
        self.set_usd_to_eur(self.app_services.yahoo_client.get_usd_to_eur())

    def click_convert_stock_data(self):
        converter : Converter = self.app_services.converter 

        len_yahoo_stock_data = len(self.yahoo_stock_data)
        len_usd_to_eur = len(self.usd_to_eur)
        if len_yahoo_stock_data != len_usd_to_eur:
            print(f"yahoo_stock_data length {len_yahoo_stock_data} != usd_to_eur length {len_usd_to_eur}")
            return

        open_list = self.yahoo_stock_data['Open'].to_list()
        high_list = self.yahoo_stock_data['High'].to_list()
        low_list = self.yahoo_stock_data['Low'].to_list()
        close_list = self.yahoo_stock_data['Close'].to_list()
        adj_close_list = self.yahoo_stock_data['Adj Close'].to_list()
        usd_to_eur_list = self.usd_to_eur['Close'].to_list()

        open_converted, _ = converter.convert_array(open_list, "USD", usd_to_eur_list, "EUR/USD")
        high_converted, _ = converter.convert_array(high_list, "USD", usd_to_eur_list, "EUR/USD")
        low_converted, _ = converter.convert_array(low_list, "USD", usd_to_eur_list, "EUR/USD")
        close_converted, _ = converter.convert_array(close_list, "USD", usd_to_eur_list, "EUR/USD")
        adj_close_converted, _ = converter.convert_array(adj_close_list, "USD", usd_to_eur_list, "EUR/USD")

        pandas_frame = pandas.DataFrame({
            'Open': open_converted,
            'High': high_converted,
            'Low': low_converted,
            'Close': close_converted,
            'Adj Close': adj_close_converted,
            'Volume': self.yahoo_stock_data['Volume'],
        }, index=self.yahoo_stock_data.index)
        pandas_frame.index.name = 'Date'

        self.set_yahoo_converted_data(pandas_frame)

    def click_add_deviation_to_converted_stock_data(self):
        if self.yahoo_converted_data.empty:
            print("yahoo_converted_data is empty")
            return
        if self.tradegate_stock_data.empty:
            print("tradegate_stock_data is empty")
            return
        if len(self.yahoo_converted_data) != len(self.tradegate_stock_data):
            len_yahoo_converted_data = len(self.yahoo_converted_data)
            len_tradegate_stock_data = len(self.tradegate_stock_data)
            print(f"yahoo_converted_data length {len_yahoo_converted_data} != tradegate_stock_data length {len_tradegate_stock_data}")
            return
        
        yahoo_converted_close_list = self.yahoo_converted_data['Close'].to_list()
        tradegate_close_list = self.tradegate_stock_data['Close'].to_list()

        def get_deviation(yahoo, tradegate) -> float:
            try:
                yahoo_num = float(yahoo)
                tradegate_num = float(tradegate)
                return round((yahoo_num / tradegate_num)-1, 4)
            except ValueError:
                #like divide by zero or something
                return 0.0


        deviation_list = [get_deviation(yahoo, tradegate)  for yahoo, tradegate in zip(yahoo_converted_close_list, tradegate_close_list)]
        self.yahoo_converted_data['deviation'] = deviation_list


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
