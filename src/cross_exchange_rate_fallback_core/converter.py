from typing import Tuple, Union
from cross_exchange_rate_fallback_core.appservices import AppServices

class Converter:
    def __init__(self, app_services : AppServices):
        self.app_services = app_services

    def convert(self, source_value, source_currency, rate, rate_unit) -> Tuple[ Union[int, float], str]:
        if not (isinstance(source_value, int) or isinstance(source_value, float)):
            raise TypeError(f"source_value must be float or int, not {type(source_value)}")
        if not isinstance(source_currency, str):
            raise TypeError(f"source_currency must be str, not {type(source_currency)}")
        if not (isinstance(rate, float) or isinstance(rate, int)):
            raise TypeError(f"rate must be float or int, not {type(rate)}")
        if not isinstance(rate_unit, str):
            raise TypeError(f"rate_unit must be str, not {type(rate_unit)}")
        #if rate_unit does not contain the source_currency, then raise ValueError
        if source_currency not in rate_unit:
            raise ValueError(f"source_currency '{source_currency}' not in rate_unit '{rate_unit}'")

        numerator, denominator = rate_unit.split("/")
        numerator = numerator.strip()
        denominator = denominator.strip()
        if source_currency == numerator:
            converted = source_value / rate
            currency = denominator
            return converted, currency
        elif source_currency == denominator:
            converted = source_value * rate
            currency = numerator
            return converted, currency

    #actual_dollars, actual_currency = self.uut.convert_array(source_euros, source_currency, rates, rate_unit)

    def convert_array(self, source_values, source_currency, rates, rate_unit) -> Tuple[ list[Union[int, float]], str]:
        if not isinstance(source_values, list):
            raise TypeError(f"source_values must be list, not {type(source_values)}")
        if not isinstance(rates, list):
            raise TypeError(f"rates must be list, not {type(rates)}")
        #other parameters are checked by convert()

        converted = []
        currency = None
        for source_value, rate in zip(source_values, rates):
            actual, currency = self.convert(source_value, source_currency, rate, rate_unit)
            converted.append(actual)
        return converted, currency