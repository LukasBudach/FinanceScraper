===================
Developer Interface
===================

This part of the documentation is meant to provide any developer looking to use
the Finance Scraper project in their own code with a detailed description of
what exactly the interface provided does, looks like and how it should be used.
It is also a great starting point for developers wanting to *get involved and
contribute* to the project!

Finance Scraper
---------------
There is one class for every data source tapped by this project. They all
use the same interface and return the same dictionary if data was found. It is
also planned to provide one general scraper class, that provides the same
interface but tapps into multiple data sources to provide a better user 
experience.

Currently the following finance scraper classes are provided:

:YahooScraper:
    provides data from finance.yahoo.com

Return Dictionaries
+++++++++++++++++++

Every time any data related to a ticker is requested by the user the raw data
is composed into a dictionary that then is returned. The following paragraph
seeks to define those dictionaries returned for access to the data by the APIs
user.

- **Ticker Data**
    This dictionary is returned whenever the function :code:`get_data(ticker)`
    is called on a scraper object. This data must always be complete. If it is
    not the function returns :code:`None` instead of this dictionary.

    Currently the following data is contained in the dictionary:

+-----------------+-----------------------------------------------------------------+
| Key             | Value                                                           |
+=================+=================================================================+
| Currency        | Currency code representing the currency of ticker's price (e.g. |
|                 | USD, EUR)                                                       |
+-----------------+-----------------------------------------------------------------+
| ETF             | Boolean indicating if the ticker belongs to an ETF_             |
+-----------------+-----------------------------------------------------------------+
| Price           | Price of one share of the holding represented by the ticker     |
+-----------------+-----------------------------------------------------------------+
| Security Name   | Name of the holding represented by the ticker                   |
+-----------------+-----------------------------------------------------------------+
| Source          | String representation of the data source (e.g. Yahoo)           |
+-----------------+-----------------------------------------------------------------+

- **Company Data**
    This dictionary is returned when the function 
    :code:`get_company_data(ticker)` is called. The data contained in the
    dictionary needs to be complete. If it isn't the function will simply
    return :code:`None`.

    Currently the dictionary contains the following data:

+-----------------+-----------------------------------------------------------------+
| Key             | Value                                                           |
+=================+=================================================================+
| Company Name    | Name of the company represented by the ticker                   |
+-----------------+-----------------------------------------------------------------+
| Description     | Description of the company provided by the data source          |
+-----------------+-----------------------------------------------------------------+
| Exchange        | Name of the exchange the ticker gets traded on (e.g. NasdaqGS)  |
+-----------------+-----------------------------------------------------------------+
| Industry        | Industry the company is active in (e.g. Specialty Retail)       |
+-----------------+-----------------------------------------------------------------+
| Sector          | Sector the company is associated with (e.g. Consumer Cyclical)  |
+-----------------+-----------------------------------------------------------------+
| Symbol          | The ticker symbol                                               |
+-----------------+-----------------------------------------------------------------+
| Website         | Company website as provided by the data source                  |
+-----------------+-----------------------------------------------------------------+


YahooScraper
++++++++++++
    
Provides an interface to collect data related to a ticker from Yahoo 
Finance.

financescraper.scraper.YahooScraper( *use_buffer=True, buffer_size=10, 
holding_time=15* )

:Parameters:
    - **use_buffer** 
        Allow the scraper to hold an internal buffer saving 
        data fetched previously for faster consecutive requests on the same ticker
    - **buffer_size** 
        Defines how many different tickers can be stored in the
        buffer until the oldest are replaced with newer ones
    - **holding_time** 
        Defines how long data should be held in the internal
        buffer in seconds before it is deemed out-of-date

:Functions:
    - **close_connection** ()
        Closes the requests Session held by the YahooScraper object. The 
        Session *cannot be reopened!*
    - **set_buffer_size** ( *size* )
        Sets the maximum amount of unique tickers that can be held within the
        internal buffer.
    - **set_holding_time** ( *holding_time* )
        Sets the maximum duration in seconds for which data is held in the
        internal buffer until it is deemed to be out of date and removed
        to be re-fetched
    - **get_data** ( *ticker* )
        Fetches data for the given *ticker* from the internal buffer or the 
        defined source. If data was retrieved it is saved in the internal
        buffer and returned as the previously defined dictionary containing the
        relevant portions of the recovered data. If the fetch was not 
        successful returns :code:`None`.
    - **get_company_data** ( *ticker* )
        Fetches data for the given *ticker* from the internal buffer or the 
        defined source. If data was retrieved it is saved in the internal
        buffer and returned as the previously defined dictionary containing the
        relevant portions of the recovered data. If the fetch was not 
        successful returns :code:`None`.

Currency Converter
------------------

Due to it's direct connection to the matter of financial data from
international markets, the Finance Scraper project provides a currency 
converter, that fetches the current exchange rate frome one (base) to another
(target) currency and converts the given amount from that base to the target
currency.

financescraper.conversions.CurrencyConverter( *target_currency_code, 
use_buffer=True, buffer_size=10, holding_time=1800* )

:Parameters:
    - **target_currency_code** 
        Currency code (e.g. USD, EUR) to which this
        converter object is going to convert to.
    - **use_buffer** 
        Allow the scraper to hold an internal buffer saving 
        data fetched previously for faster consecutive requests on the same ticker
    - **buffer_size**  
        Defines how many different tickers can be stored in the
        buffer until the oldest are replaced with newer ones
    - **holding_time** 
        Defines how long data should be held in the internal
        buffer in seconds before it is deemed out-of-date

:Functions:
    - **set_buffer_size** ( *size* )
        Sets the maximum amount of unique tickers that can be held within the
        internal buffer.
    - **set_holding_time** ( *holding_time* )
        Sets the maximum duration in seconds for which data is held in the
        internal buffer until it is deemed to be out of date and removed
        to be re-fetched
    - **convert** ( *base_currency_code, amount* )
        Returns *amount* converted from the base currency defined by 
        *base_currency_code* to the previously defined target currency of the
        object. Returns :code:`None` if no conversion could be found (this is
        most likely the case when *base_currency_code* is not valid)

.. _ETF: https://www.investopedia.com/terms/e/etf.asp