from cross_exchange_rate_fallback_core.appmodel import AppModel
from cross_exchange_rate_fallback_core.appservices import AppServices
from cross_exchange_rate_fallback_core.yahooclient import YahooClient


def before_all(context):
    context.app_services = AppServices()
    context.app_services.initialize_service("yahoo_client", YahooClient)
    context.app_model = AppModel(context.app_services)

def after_all(context):
    pass