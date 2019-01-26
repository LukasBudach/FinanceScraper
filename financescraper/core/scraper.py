import requests
import json
import logging

from ..util import circular_buffer


class YahooScraper:
    def __init__(self, use_buffer=True, buffer_size=10, holding_time=15):
        self.session = requests.Session()
        self.url = 'https://finance.yahoo.com/quote/'
        self.session.get('https://finance.yahoo.com')

        self.use_buffer = use_buffer

        if use_buffer:
            # add internal buffer to reduce load times on rapid, repeated requests
            self.buffer = circular_buffer.CircularBuffer(buffer_size, holding_time)

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        self.session.close()

    def set_buffer_size(self, size):
        if self.use_buffer:
            self.buffer.set_size(size)

    def set_holding_time(self, holding_time):
        if self.use_buffer:
            self.buffer.set_holding_time(holding_time)

    def _fetch_data(self, ticker):
        res = self.session.get(self.url + ticker)
        if not (res.status_code == requests.codes.ok):
            logging.error('data fetching failed')
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

    def get_data(self, ticker):
        if self.use_buffer:
            data_object = self.buffer.get(ticker)
        else:
            data_object = None

        if data_object is None:
            data_object = self._fetch_data(ticker)

        if data_object is None:
            return None

        data = {}

        try:
            quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
            data['Source'] = 'Yahoo'
            data['Price'] = quote_summary['financialData']['currentPrice']['raw']
            data['Currency'] = quote_summary['price']['currency']
            data['Security Name'] = quote_summary['price']['longName']
            data['ETF'] = (quote_summary['price']['quoteType'] == 'ETF')
            data['Valid'] = True
        except KeyError:
            logging.warning("No valid data found for " + ticker)
            return None

        return data

    def get_company_data(self, ticker):
        if self.use_buffer:
            data_object = self.buffer.get(ticker)
        else:
            data_object = None

        if data_object is None:
            data_object = self._fetch_data(ticker)

        if data_object is None:
            return None

        data = {'company': {'symbol': ticker}}

        try:
            quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
            company = data['company']
            company['companyName'] = quote_summary['price']['longName']
            company['exchange'] = quote_summary['price']['exchangeName']
            company['industry'] = quote_summary['summaryProfile']['industry']
            company['website'] = quote_summary['summaryProfile']['website']
            company['description'] = quote_summary['summaryProfile']['longBusinessSummary']
            company['CEO'] = ''
            company['issueType'] = ''
            company['sector'] = quote_summary['summaryProfile']['sector']
            company['tags'] = []
        except KeyError:
            logging.warning("No valid company data found for " + ticker)
            return None

        return data
