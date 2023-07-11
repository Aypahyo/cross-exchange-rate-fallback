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