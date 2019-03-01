==========
Quickstart
==========

Make a Ticker request
---------------------

This is the main reason you are probably going to want to use this API for your
own project. Finance Scraper is aimimg to provide multiple classes, one for
access to a single of its own data sources. As of version 0.2.0 there is only
one source - yahoo finance.

Due to this architecture you are going to need to get yourself a scraper object
to make your requests. This object will internally keep a Session_ open, so for
request efficiency it is recommended to keep your scraper object as long as you
are planning to make requests to a specific source.

Here is an example of how you would create the :ref:`finance-scraper` object - a
scraper that combines multiple other ones to deliver results faster and more
complete than a single scraper could - and use it to fetch data for a specific
ticker:

.. code-block:: Python

  from financescraper import scraper
  my_scraper = scraper.FinanceScraper()
  data = my_scraper.get_data('AMZN')

The *get_data(ticker)* method will return a TickerData object if the data could
be recovered for the ticker and **None** if not.

If you want to additionally get some more information on the holding/company
behind your ticker, you can do so by fetching the company data like so:

.. code-block:: Python

  from financescraper import scraper
  my_scraper = scraper.FinanceScraper()
  data = my_scraper.get_company_data('AMZN')

The *get_company_data(ticker)* method will return a CompanyData object if the
data could be recovered for the ticker and **None** if not.

For more information on the data object check out the section 
:ref:`ret-data-objects` in the interface reference.

Convert between currencies
--------------------------

As this is closely related to the issue of fetching financial data from
international markets, Finance Scraper does also provide a way to convert in
between currencies using the current exchange rates as provided on yahoo
finance.

In order to use this feature you will have to know the currency codes (EUR for
€, USD for $, CAD for $ and so on) for both your current currency and your
desired currency. If you know this you can create yourself a CurrencyConverter
object and initialize it with your desired currency.

As with the FinanceScraper you are going to want to keep your Converter object
as long as you need it, because it does use the :ref:`yahoo-scraper` internally which
keeps a Session_ open for improved performance.

Here is an example of how you would create the CurrencyConverter object to
convert some currency to USD and how you can then use it to get your prices
converted:

.. code-block:: Python

  from financescraper import conversions
  usd_converter = conversions.CurrencyConverter('USD')
  amount_in_usd = usd_converter.convert('EUR', 100))

If you want to see more code examples please take a look at the bin folder on
this projects repository_.

For more information and customizations check out the in-depth **API
documentation**.

.. _Session: http://docs.python-requests.org/en/master/user/advanced/#session-objects
.. _ETF: https://www.investopedia.com/terms/e/etf.asp
.. _repository: https://github.com/LukasBudach/FinanceScraper