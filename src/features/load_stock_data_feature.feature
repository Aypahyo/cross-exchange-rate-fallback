Feature: Load Stock Data

  Scenario: Load yahoo stock data for a well traded symbol
  Given I see the 'stock' page
  And I stock symbol 'GOOG' is entered in the 'stock_search_term'
  And 'yahoo_stock_data' is empty
  When I click the 'update_stock_data' button
  Then 'yahoo_stock_data' should not be empty

  Scenario: Load tradegate stock data for a well traded symbol
  Given I see the 'stock' page
  And I stock symbol 'GOOG' is entered in the 'stock_search_term'
  And 'tradegate_stock_data' is empty
  When I click the 'update_stock_data' button
  Then 'tradegate_stock_data' should not be empty

  Scenario: Load yahoo exchange rate data from USD to EUR
  Given I see the 'stock' page
  And 'usd_to_eur' is empty
  When I click the 'update_exchange_rate_data' button
  Then 'usd_to_eur' should not be empty

  Scenario: Convert yahoo stock from UST to EUR
  Given I see the 'stock' page
  And stock data is loaded for 'GOOG'
  And exchange usd_to_eur_rate data is loaded 
  And 'yahoo_converted_data' is empty
  When I click the 'convert_stock_data' button
  Then 'yahoo_converted_data' should not be empty

  Scenario: Add deviation to converted stock data
  Given I see the 'stock' page
  And stock data is converted for 'GOOG'
  When I click the 'add_deviation_to_converted_stock_data' button
  Then 'yahoo_converted_data' has a column 'deviation'