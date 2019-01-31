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

.. _ret-data-objects:

Returned Data Objects
+++++++++++++++++++++

When a request is made to a scraper object provided by this project, a data 
object corresponding to the requests purpose is returned. The objects do
internally save the fetched data in attributes defined as slots. They can be
accessed by calling <yourObject>.<attributeName>

Currently the following data classes are defined. If you don't find the data
you require, put in an issue on this project's repository_ for it to be
considered for inclusion with the next version release.

- **TickerData**
    A TickerData object is created and returned whenever the function
    :code:`get_data(ticker)` is called on a scraper object. The fetched data 
    must always include all of the fields provided by the TickerData object. If
    it is not, the function returns :code:`None` instead of this dictionary.

    Currently the following data is supported in the TickerData object:

+-----------------+-----------------------------------------------------------------+
| Attribute       | Value                                                           |
+=================+=================================================================+
| currency        | Currency code representing the currency of ticker's price (e.g. |
|                 | USD, EUR)                                                       |
+-----------------+-----------------------------------------------------------------+
| etf             | Boolean indicating if the ticker belongs to an ETF_             |
+-----------------+-----------------------------------------------------------------+
| name            | Name of the holding represented by the ticker                   |
+-----------------+-----------------------------------------------------------------+
| price           | Price of one share of the holding represented by the ticker     |
+-----------------+-----------------------------------------------------------------+
| source          | String representation of the data source (e.g. Yahoo)           |
+-----------------+-----------------------------------------------------------------+

- **CompanyData**
    The CompanyData object is returned when the function 
    :code:`get_company_data(ticker)` is called. The data contained in the
    object's attributes needs to be complete in the fetched JSON. If it isn't 
    the function will simply return :code:`None`.

    Currently the CompanyData object contains the following attributes:

+-----------------+-----------------------------------------------------------------+
| Attribute       | Value                                                           |
+=================+=================================================================+
| description     | Description of the company provided by the data source          |
+-----------------+-----------------------------------------------------------------+
| exchange        | Name of the exchange the ticker gets traded on (e.g. NasdaqGS)  |
+-----------------+-----------------------------------------------------------------+
| industry        | Industry the company is active in (e.g. Specialty Retail)       |
+-----------------+-----------------------------------------------------------------+
| name            | Name of the company represented by the ticker                   |
+-----------------+-----------------------------------------------------------------+
| sector          | Sector the company is associated with (e.g. Consumer Cyclical)  |
+-----------------+-----------------------------------------------------------------+
| symbol          | The ticker symbol                                               |
+-----------------+-----------------------------------------------------------------+
| website         | Company website as provided by the data source                  |
+-----------------+-----------------------------------------------------------------+

.. _yahoo-scraper:

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
        buffer and returned as the previously defined TickerData object 
        containing the relevant portions of the recovered data. If the fetch
        was not successful returns :code:`None`.
    - **get_company_data** ( *ticker* )
        Fetches data for the given *ticker* from the internal buffer or the 
        defined source. If data was retrieved it is saved in the internal
        buffer and returned as the previously defined CompanyData object
        containing the relevant portions of the recovered data. If the fetch
        was not successful returns :code:`None`.

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
.. _repository: https://github.com/LukasBudach/FinanceScraper