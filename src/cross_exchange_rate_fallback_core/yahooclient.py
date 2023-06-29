import pandas
import yfinance as yf
from cross_exchange_rate_fallback_core.appservices import AppServices

class YahooClient:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services

    def get_stock_data(self, symbol: str) -> pandas.core.frame.DataFrame:
        if symbol is None or symbol == "":
            return pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        if not isinstance(symbol, str):
            raise TypeError(f"symbol must be a string, but was {type(symbol)}")
        symbol = self.get_symbol_from_isin(symbol)
        data : pandas.core.frame.DataFrame = yf.download(symbol, start='2023-06-01', end='2023-06-30', progress=False)
        if not isinstance(data, pandas.core.frame.DataFrame):
            raise TypeError(f"data must be a pandas.core.frame.DataFrame, but was {type(data)}")
        return data
    
    def get_symbol_from_isin(self, isin: str) -> str:
        if isin is None:
            isin = ""
        if not isinstance(isin, str):
            raise TypeError(f"isin must be a string, but was {type(isin)}")
        data = yf.Ticker(isin)
        return data.info['symbol']