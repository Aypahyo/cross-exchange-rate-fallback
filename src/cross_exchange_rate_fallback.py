from cross_exchange_rate_fallback_core.appservices import AppServices
from cross_exchange_rate_fallback_core.appmodel import AppModel
from cross_exchange_rate_fallback_core.tradegateclient import TradegateClient
from cross_exchange_rate_fallback_core.yahooclient import YahooClient
from cross_exchange_rate_fallback_core.stockpagemodel import StockPageModel


def main():
    app_services = AppServices()
    app_services.initialize_service("yahoo_client", YahooClient)
    app_services.initialize_service("tradegate_client", TradegateClient)
    app_model = AppModel(app_services)
    stockpage : StockPageModel = app_model.get_pagemodel("stock")
    stockpage.stock_search_term = "US42309B4023"
    stockpage.click_update_stock_data()
    print("Yahoo Stock Data:")
    print(stockpage.yahoo_stock_data)
    print("Tradegate Stock Data:")
    print(stockpage.tradegate_stock_data)

if __name__ == "__main__":
    main()