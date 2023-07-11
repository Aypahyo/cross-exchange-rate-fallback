# Cross Exchange Rate Fallback Service

This repository contains an experimental implementation of a service designed to provide reliable and accurate exchange rates data, even when the primary source is not available. The service uses a strategy pattern to switch between various sources of exchange rates data, ultimately ensuring continuous service.

## Overview

The service works as follows:

1. It tries to fetch the exchange rates data from the primary source (e.g., a specific stock exchange).
2. If the primary source is not available or does not provide data for a specific asset, the service switches to a fallback strategy. The fallback strategy involves fetching the data from the last known value.
3. If the last known value is not available or too old to be reliable, the service switches to an alternative strategy. This involves fetching the data from a free API, like Yahoo's finance API, and converting the asset value into Euros using the current exchange rate.

## Motivation

This service was inspired by the challenges faced when dealing with illiquid assets or assets with small market caps. These assets may not always have readily available and up-to-date exchange rates data. By switching between different strategies, this service ensures that we always have a best possible estimate of an asset's value in Euros.

## Testing options

```bash
python3 -m unittest discover -s tests -p *_unit.py
python3 -m unittest discover -s tests -p *_component.py
python3 -m behave
src/run_all_tests.sh
src/run_docker_all_tests.sh
```

## for later

when I write my blog entry on this, I should include a list of nano-cap stocks, e.g. from here:

<https://stockanalysis.com/list/nano-cap-stocks/>
