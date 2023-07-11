import datetime
import re
import pandas
import requests
from cross_exchange_rate_fallback_core.appservices import AppServices

class TradegateClient:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services

    def get_stock_data(self, symbol: str) -> pandas.core.frame.DataFrame:
        
        def fetch_data(url, isin, params=None):
            response = requests.get(url, params=params)
            if response.status_code != 200:
                raise Exception(f"Request failed with status code {response.status_code} url: {url} params: {params}")
            return response.json()

        if symbol is None:
            symbol = ""

        if not isinstance(symbol, str):
            raise TypeError(f"symbol must be str, not {type(symbol)}")

        # Get ISIN for Symbol
        isin = self.getISIN(symbol)
        if isin is None:
            return pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

        # Get Instrument Data for Apple
        instrument_url = f"https://api.onvista.de/api/v1/stocks/ISIN:{isin}/snapshot"
        instrument_data = fetch_data(instrument_url, isin)

        # Find the appropriate notation
        notation = None
        for quote in instrument_data["quoteList"]["list"]:
            if quote["market"]["name"] == "Tradegate":
                notation = quote
                break

        if notation is None:
            return pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        
        # Get Quotes for Apple
        quotes_url = f"https://api.onvista.de/api/v1/instruments/STOCK/{instrument_data['instrument']['entityValue']}/chart_history"
        params = {
            "endDate": "2023-06-30",
            "idNotation": notation["market"]["idNotation"],
            #"resolution": "1d",
            "startDate": "2023-06-01",
        }
        quotes_data = fetch_data(quotes_url, isin, params)

        # Create pandas dataframe
        df = pandas.DataFrame({
            "Open": quotes_data['first'],
            "High": quotes_data['high'],
            "Low": quotes_data['low'],
            "Close": quotes_data['last'],
            "Adj Close": quotes_data['last'], # Adjusted Close data is typically not directly provided in the fetched data
            "Volume": quotes_data['volume'],
        }, index=[datetime.datetime.fromtimestamp(ts) for ts in quotes_data['datetimeLast']])
        df.index.name = "Date"


        return df
        
    def getISIN(self, symbol: str) -> str:
        if symbol is None or not isinstance(symbol, str):
            return None

        symbol_cleaned = symbol
        symbol_cleaned = symbol_cleaned.upper()
        symbol_cleaned = symbol_cleaned.replace(" ", "")
        symbol_cleaned = symbol_cleaned.strip()
        symbol_cleaned = re.sub(r"((?<=(^[A-Z]{2}))-)|(-(?=\d$))", "", symbol_cleaned) # Removes dashes from common notation (e.g. US-037833100-5 -> US0378331005)

        if len(symbol_cleaned) == 12 and re.match(r"^[A-Z]{2}[A-Z0-9]{9}\d$", symbol_cleaned) is not None:
            # The symbol follows the ISIN format
            digits = [str(ord(c) - 55) if c.isalpha() else c for c in symbol_cleaned[0:11]]
            digits = [int(c) for c in [c for c in "".join(digits)]]
            digits.reverse() # reverse order - we need to start with the last digit
            def index_aware_doubeling(digit, reverse_index):
                if digit >= 5 and reverse_index in range(0, 24, 2): ret = digit * 2 - 9
                elif digit < 5 and reverse_index in range(0, 24, 2): ret = digit * 2
                else: ret = digit
                return ret
            digits = [index_aware_doubeling(digit, reverse_index) for reverse_index, digit in enumerate(digits)]
            digits.reverse() # original order
            checksum = 10 - sum(digits) % 10
            if checksum == 10: checksum = 0
            if checksum == int(symbol_cleaned[11]):
                return symbol_cleaned # looks like a valid ISIN
            else:
                # looks like an ISIN, but the checksum is wrong
                return None
        elif len(symbol_cleaned) > 0: # minimal viable ticker length is 1 - example: "F" for Ford
            # todo maybe - at this point we would need to query an API to get the ISIN
            # I am going way too deep for this mini example so I will just hard code a few examples
            # ultimately I could build a database of well known tickers and their ISINs
            # there is an idea for a future project - SAAS for ISIN lookup in exchange for a small fee

            well_known_tickers = {}
            well_known_tickers["AAPL"] = "US0378331005"
            well_known_tickers["MSFT"] = "US5949181045"
            well_known_tickers["AMZN"] = "US0231351067"
            well_known_tickers["GOOG"] = "US02079K3059"
            well_known_tickers["GOOGL"] = "US02079K1079"
            well_known_tickers["FB"] = "US30303M1027"
            well_known_tickers["TSLA"] = "US88160R1014"
            well_known_tickers["NVDA"] = "US67066G1040"
            well_known_tickers["JPM"] = "US46625H1005"
            well_known_tickers["JNJ"] = "US4781601046"
            well_known_tickers["V"] = "US92826C8394"
            well_known_tickers["PG"] = "US7427181091"
            well_known_tickers["UNH"] = "US91324P1021"
            well_known_tickers["HD"] = "US4370761029"
            well_known_tickers["MA"] = "US57636Q1040"
            well_known_tickers["BAC"] = "US0605051046"
            well_known_tickers["DIS"] = "US2546871060"
            well_known_tickers["PYPL"] = "US70450Y1038"
            well_known_tickers["ADBE"] = "US00724F1012"
            well_known_tickers["CMCSA"] = "US20030N1019"
            well_known_tickers["NFLX"] = "US64110L1061"
            well_known_tickers["INTC"] = "US4581401001"
            well_known_tickers["VZ"] = "US92343V1044"
            well_known_tickers["KO"] = "US1912161007"
            well_known_tickers["T"] = "US00206R1023"
            well_known_tickers["PFE"] = "US7170811035"
            well_known_tickers["NKE"] = "US6541061031"
            well_known_tickers["MRK"] = "US58933Y1055"
            well_known_tickers["CRM"] = "US79466L3024"
            well_known_tickers["WMT"] = "US9311421039"
            well_known_tickers["PEP"] = "US7134481081"
            well_known_tickers["ABT"] = "US0028241000"
            well_known_tickers["CSCO"] = "US17275R1023"
            well_known_tickers["XOM"] = "US30231G1022"
            well_known_tickers["CVX"] = "US1667641005"
            well_known_tickers["BABA"] = "US01609W1027"
            well_known_tickers["ORCL"] = "US68389X1054"
            well_known_tickers["ACN"] = "IE00B4BNMY34"
            well_known_tickers["TMO"] = "US8835561023"
            well_known_tickers["AVGO"] = "US11135F1012"
            well_known_tickers["NVS"] = "US66987V1098"
            well_known_tickers["QCOM"] = "US7475251036"
            well_known_tickers["TXN"] = "US8825081040"
            well_known_tickers["COST"] = "US22160K1051"
            well_known_tickers["NEE"] = "US6643971061"
            well_known_tickers["DHR"] = "US23331A1097"

            if symbol_cleaned in well_known_tickers:
                return well_known_tickers[symbol_cleaned]
            else:
                return None
        else:
            return None
