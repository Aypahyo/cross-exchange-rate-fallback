# Cross Exchange Rate Fallback Service

This repository contains an experimental implementation of a service designed to provide reliable and accurate exchange rates data, even when the primary source is not available. The service uses a strategy pattern to switch between various sources of exchange rates data, ultimately ensuring continuous service.

## Overview

The service works as follows:

* It queries stock data and exchange rate sources with a fixed time frame.
* It converts the data to a common currency (EUR)
* It calculates the percentage deviation between the two data sources
* It prints the data frames to the console

## Motivation

This service was inspired by the challenges faced when dealing with illiquid assets or assets with small market caps. These assets may not always have readily available and up-to-date exchange rates data. By switching between different strategies, this service ensures that we always have a best possible estimate of an asset's value in Euros.

This implementation explores stock data source options and combining them in order to determine feasability of that strategy.

## Testing options

```bash
python3 -m unittest discover -s tests -p *_unit.py
python3 -m unittest discover -s tests -p *_component.py
python3 -m behave
src/run_all_tests.sh
src/run_docker_all_tests.sh
```

## Sample usage

```bash
python3 ./src/cross_exchange_rate_fallback.py AAPL
python3 ./src/cross_exchange_rate_fallback.py GOOG
python3 ./src/cross_exchange_rate_fallback.py US42309B4023
```

AAPL and GOOG are examples of well traded stocks, while US42309B4023 is an example of a nanocap stock.
AAPL and GOOG are enriched with percentage deviation that compares known Tradegate with Converted from Yahoo data.
US42309B4023 has no TradeGate data, so there is no percentage deviation.
