import requests
import json
import logging

from enum import Enum
from abc import ABC, abstractmethod

from financescraper.datacontainer import circular_buffer, container


class ScraperApproach(Enum):
    FAST = 1
    BALANCED = 2
    THOROUGH = 3


class Scraper(ABC):
    def __init__(self, source, use_buffer, buffer_size, holding_time):
        # open a requests session for more efficient access behavior
        self.session = requests.Session()
        if source == 'Yahoo':
            self.url = 'https://finance.yahoo.com/quote/'
            self.session.get('https://finance.yahoo.com')
        elif source == 'IEX':
            self.url = 'https://api.iextrading.com/1.0/stock/'
            self.session.get('https://api.iextrading.com/1.0/')
        elif source == 'General':
            self.url = None
            self.session = None

        self.use_buffer = use_buffer

        if use_buffer:
            # add internal buffer to reduce load times on rapid, repeated requests
            self.buffer = circular_buffer.CircularBuffer(buffer_size, holding_time)

    def __del__(self):
        # make sure to close the session when a scraper is disposed of
        self.close_connection()

    # closes the requests session held by the scraper !there is no way to re-open the session!
    def close_connection(self):
        self.session.close()

    # sets the amount of stocks that will be buffered internally
    def set_buffer_size(self, size):
        if self.use_buffer:
            self.buffer.set_size(size)

    # sets the time after which stocks need to be re-loaded in seconds
    def set_holding_time(self, holding_time):
        if self.use_buffer:
            self.buffer.set_holding_time(holding_time)

    # internal function that either gets data from the buffer or starts the fetch
    def _get_data_object(self, ticker):
        if self.use_buffer:
            data_object = self.buffer.get(ticker)
        else:
            data_object = None

        if data_object is None:
            data_object = self._fetch_data(ticker)
        elif self.use_buffer:
            self.buffer.refresh(ticker)

        return data_object

    # internal function executing the html request for a given ticker
    @abstractmethod
    def _fetch_data(self, ticker):  # pragma: no cover
        pass

    # interface method returning a TickerData object
    @abstractmethod
    def get_data(self, ticker):  # pragma: no cover
        pass

    # interface method returning a CompanyData object
    @abstractmethod
    def get_company_data(self, ticker):  # pragma: no cover
        pass


class YahooScraper(Scraper):
    def __init__(self, use_buffer=True, buffer_size=10, holding_time=15):
        super().__init__('Yahoo', use_buffer, buffer_size, holding_time)

    def _fetch_data(self, ticker):
        res = self.session.get(self.url + ticker)
        if not (res.status_code == requests.codes.ok):  # pragma: no cover
            logging.error('[YahooScraper] Data fetching failed for ' + ticker)
            return None

        raw_data = res.text

        object_start = raw_data.find("root.App.main") + 16
        object_end = raw_data.find("</script>", object_start) - 12
        data_json = raw_data[object_start: object_end]

        data_object = json.loads(data_json)

        if self.use_buffer:
            self.buffer.add(ticker, data_object)

        return data_object

    # returns a dictionary containing all relevant financial data associated with a ticker
    def get_data(self, ticker):
        data_object = self._get_data_object(ticker)
        if data_object is None:  # pragma: no cover
            return None

        data = container.TickerData('Yahoo')

        try:
            quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
            data.currency = quote_summary['price']['currency']
            data.etf = (quote_summary['price']['quoteType'] == 'ETF')
            data.name = quote_summary['price']['longName']
            data.price = quote_summary['price']['regularMarketPrice']['raw']
        except KeyError as e:
            logging.warning("[YahooScraper] No valid data found for " + ticker + '. Missing key: ' + e.args[0])
            return None

        return data

    # returns a dictionary containing all relevant company data associated with a ticker
    def get_company_data(self, ticker):
        data_object = self._get_data_object(ticker)
        if data_object is None:  # pragma: no cover
            return None

        data = container.CompanyData('Yahoo')

        try:
            quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
            data.description = quote_summary['summaryProfile']['longBusinessSummary']
            data.exchange = quote_summary['price']['exchangeName']
            data.industry = quote_summary['summaryProfile']['industry']
            data.name = quote_summary['price']['longName']
            data.sector = quote_summary['summaryProfile']['sector']
            data.symbol = ticker
            data.website = quote_summary['summaryProfile']['website']
        except KeyError as e:
            logging.warning("[YahooScraper] No valid company data found for " + ticker + '. Missing key: ' + e.args[0])
            return None

        return data


class IEXScraper(Scraper):
    def __init__(self, use_buffer=True, buffer_size=10, holding_time=15):
        super().__init__('IEX', use_buffer, buffer_size, holding_time)

    def _fetch_data(self, ticker):
        res = self.session.get(self.url + ticker + '/batch?types=quote,company')
        if not (res.status_code == requests.codes.ok):  # pragma: no cover
            logging.error('[IEXScraper] Data fetching failed for ' + ticker)
            return None

        data_object = json.loads(res.text)

        if self.use_buffer:
            self.buffer.add(ticker, data_object)

        return data_object

    def get_data(self, ticker):
        data_object = self._get_data_object(ticker)
        if data_object is None:
            return None

        data = container.TickerData('IEX')

        try:
            quote = data_object['quote']
            data.currency = 'USD'
            data.etf = (data_object['company']['issueType'] == 'et')
            data.name = quote['companyName']
            data.price = quote['latestPrice']
        except KeyError as e:  # pragma: no cover
            logging.warning("[IEXScraper] No valid data found for " + ticker + '. Missing key: ' + e.args[0])
            return None

        return data

    def get_company_data(self, ticker):
        data_object = self._get_data_object(ticker)
        if data_object is None:
            return None

        data = container.CompanyData('IEX')

        try:
            company = data_object['company']
            data.description = company['description']
            data.exchange = company['exchange']
            data.industry = company['industry']
            data.name = company['companyName']
            data.sector = company['sector']
            data.symbol = ticker
            data.website = company['website']
        except KeyError as e:  # pragma: no cover
            logging.warning("[IEXScraper] No valid company data found for " + ticker + '. Missing key: ' + e.args[0])
            return None

        return data


class FinanceScraper(Scraper):
    def __init__(self, use_buffer=True, buffer_size=10, holding_time=15, approach=ScraperApproach.BALANCED):
        super().__init__('General', use_buffer, buffer_size, holding_time)
        self.scraper = {
            '0': IEXScraper(use_buffer, buffer_size, holding_time),
            '1': YahooScraper(use_buffer, buffer_size, holding_time)
        }
        self.approach = approach

    def __del__(self):
        for scraper in self.scraper:
            del scraper
        self.scraper = None

    def set_buffer_size(self, size):
        super().set_buffer_size(size)
        idx = 0
        while idx < self.scraper.__len__():
            self.scraper.get(str(idx)).set_buffer_size(size)
            idx += 1

    def set_holding_time(self, holding_time):
        super().set_holding_time(holding_time)
        idx = 0
        while idx < self.scraper.__len__():
            self.scraper.get(str(idx)).set_holding_time(holding_time)
            idx += 1

    def set_approach(self, approach):
        self.approach = approach

    def _fetch_data(self, ticker):
        raise(Exception('The FinanceScraper object is not meant to implement _fetch_data'))

    def close_connection(self):
        raise(Exception('The FinanceScraper object does not hold an open requests Session object.'))

    # returns a dictionary containing all relevant financial data associated with a ticker
    def get_data(self, ticker):
        data_object = None
        loops = 0

        if self.approach == ScraperApproach.FAST:
            data_object = self.scraper.get(str(0)).get_data(ticker)
        elif self.approach == ScraperApproach.BALANCED:
            while (data_object is None) and (loops < self.scraper.__len__()):
                data_object = self.scraper.get(str(loops)).get_data(ticker)
                loops += 1
        elif self.approach == ScraperApproach.THOROUGH:
            while loops < self.scraper.__len__():
                current = self.scraper.get(str(loops)).get_data(ticker)
                data_object = current if data_object is None else data_object.merge(current)
                loops += 1

        return data_object

    # returns a dictionary containing all relevant company data associated with a ticker
    def get_company_data(self, ticker):
        data_object = None
        loops = 0

        if self.approach == ScraperApproach.FAST:
            data_object = self.scraper.get(str(0)).get_company_data(ticker)
        elif self.approach == ScraperApproach.BALANCED:
            while (data_object is None) and (loops < self.scraper.__len__()):
                data_object = self.scraper.get(str(loops)).get_company_data(ticker)
                loops += 1
        elif self.approach == ScraperApproach.THOROUGH:
            while loops < self.scraper.__len__():
                current = self.scraper.get(str(loops)).get_company_data(ticker)
                data_object = current if data_object is None else data_object.merge(current)
                loops += 1

        return data_object
