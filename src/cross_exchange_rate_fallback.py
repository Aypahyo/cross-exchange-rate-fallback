from cross_exchange_rate_fallback_core.appservices import AppServices
from cross_exchange_rate_fallback_core.appmodel import AppModel
from cross_exchange_rate_fallback_core.converter import Converter
from cross_exchange_rate_fallback_core.tradegateclient import TradegateClient
from cross_exchange_rate_fallback_core.yahooclient import YahooClient
from cross_exchange_rate_fallback_core.stockpagemodel import StockPageModel


def main():
    app_services = AppServices()
    app_services.initialize_service("yahoo_client", YahooClient)
    app_services.initialize_service("tradegate_client", TradegateClient)
    app_services.initialize_service("converter", Converter)
    app_model = AppModel(app_services)
    stockpage : StockPageModel = app_model.get_pagemodel("stock")
    stockpage.stock_search_term = "US42309B4023"
    #stockpage.stock_search_term = "GOOG"
    stockpage.click_update_stock_data()
    stockpage.click_update_exchange_rate_data()
    stockpage.click_convert_stock_data()

    print("Yahoo Stock Data (USD):")
    print(stockpage.yahoo_stock_data)
    print("Tradegate Stock Data (EUR):")
    print(stockpage.tradegate_stock_data)
    print("USD to EUR Exchange Rate Data:")
    print(stockpage.usd_to_eur)
    print("Yahoo Stock Data converted to EUR:")
    print(stockpage.yahoo_converted_data)

if __name__ == "__main__":
    main()