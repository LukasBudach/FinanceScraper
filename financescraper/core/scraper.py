import requests
import json
import logging

from abc import ABC, abstractmethod

from financescraper.datacontainer import circular_buffer, container


class Scraper(ABC):
    def __init__(self, source, use_buffer, buffer_size, holding_time):
        # open a requests session for more efficient access behavior
        self.session = requests.Session()
        if source == 'Yahoo':
            self.url = 'https://finance.yahoo.com/quote/'
            self.session.get('https://finance.yahoo.com')
        elif source == 'Google':
            self.url = 'https://www.google.com/search?q='
            self.session.get('https://www.google.com')

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

    # internal function executing the html request for a given ticker
    def _fetch_data(self, ticker):
        res = self.session.get(self.url + ticker)
        if not (res.status_code == requests.codes.ok):
            logging.error('Data fetching failed for ' + ticker)
            return None

        raw_data = res.text

        object_start = raw_data.find("root.App.main") + 16
        object_end = raw_data.find("</script>", object_start) - 12
        data_json = raw_data[object_start: object_end]

        data_object = json.loads(data_json)

        if self.use_buffer:
            self.buffer.add(ticker, data_object)

        else:
            if self.use_buffer:
                self.buffer.refresh(ticker)

        return data_object

    @abstractmethod
    def get_data(self, ticker):
        pass

    @abstractmethod
    def get_company_data(self, ticker):
        pass


class YahooScraper(Scraper):
    def __init__(self, use_buffer=True, buffer_size=10, holding_time=15):
        super().__init__('Yahoo', use_buffer, buffer_size, holding_time)

    # returns a dictionary containing all relevant financial data associated with a ticker
    def get_data(self, ticker):
        if self.use_buffer:
            data_object = self.buffer.get(ticker)
        else:
            data_object = None

        if data_object is None:
            data_object = self._fetch_data(ticker)

        if data_object is None:
            return None

        data = container.TickerData('Yahoo')

        try:
            quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
            data.currency = quote_summary['price']['currency']
            data.etf = (quote_summary['price']['quoteType'] == 'ETF')
            data.name = quote_summary['price']['longName']
            data.price = quote_summary['price']['regularMarketPrice']['raw']
        except KeyError as e:
            logging.warning("No valid data found for " + ticker + '. Missing key: ' + e.args[0])
            return None

        return data

    # returns a dictionary containing all relevant company data associated with a ticker
    def get_company_data(self, ticker):
        if self.use_buffer:
            data_object = self.buffer.get(ticker)
        else:
            data_object = None

        if data_object is None:
            data_object = self._fetch_data(ticker)

        if data_object is None:
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
            logging.warning("No valid company data found for " + ticker + '. Missing key: ' + e.args[0])
            return None

        return data
