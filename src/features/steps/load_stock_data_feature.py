from behave import given, when, then
import pandas
from cross_exchange_rate_fallback_core import appmodel # type: ignore

@given(u'I see the \'{page}\' page')
def i_see_the_page(context, page):
    context.current_pagemodel = context.app_model.get_pagemodel(page)

@given(u'I stock symbol \'{symbol}\' is entered in the \'{field}\'')
def i_stock_symbol_is_entered_in_the_field(context, symbol, field):
    context.current_pagemodel.set_field(field, symbol)

@given(u'\'{stock_data}\' is empty')
def stock_data_is_empty(context, stock_data):
    empty_frame = pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    context.current_pagemodel.set_field(stock_data, empty_frame)

@when(u'I click the \'{button}\' button')
def i_click_the_button(context, button):
    context.current_pagemodel.click(button)

@then(u'\'{stock_data}\' should not be empty')
def stock_data_should_not_be_empty(context, stock_data):
    expected_str = str(pandas.core.frame.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']))
    actual_str = str(context.current_pagemodel.get_field(stock_data))
    assert expected_str != actual_str, f"Expected: {expected_str}, Actual: {actual_str}"
