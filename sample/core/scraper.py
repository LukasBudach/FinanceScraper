import requests
import json
from ..util import circular_buffer


class YahooScraper:
    def __init__(self, buffer_size):
        self.session = requests.Session()
        self.url = 'https://finance.yahoo.com/quote/'
        self.session.get('https://finance.yahoo.com')

        # add dictionary to internal buffer to reduce load times on repeated requests
        self.buffer = circular_buffer.CircularBuffer(buffer_size)

    def set_buffer_size(self, size):
        self.buffer.set_size(size)

    def get_data(self, ticker):
        data_object = self.buffer.get(ticker)
        if data_object is None:
            res = self.session.get(self.url + ticker)
            if not (res.status_code == requests.codes.ok):
                print('[ERR] data fetching failed')
                return None

            raw_data = res.text

            object_start = raw_data.find("root.App.main") + 16
            object_end = raw_data.find("</script>", object_start) - 12
            data_json = raw_data[object_start: object_end]

            data_object = json.loads(data_json)

            self.buffer.add(ticker, data_object)
        else:
            self.buffer.refresh(ticker)

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
            print("[WARN] No valid data found for " + ticker)

        return data

    def get_company_data(self, ticker):
        data_object = self.buffer.get(ticker)
        if data_object is None:
            res = self.session.get(self.url + ticker)
            if not (res.status_code == requests.codes.ok):
                print('[ERR] data fetching failed')
                return None

            raw_data = res.text

            object_start = raw_data.find("root.App.main") + 16
            object_end = raw_data.find("</script>", object_start) - 12
            data_json = raw_data[object_start: object_end]

            data_object = json.loads(data_json)

            self.buffer.add(ticker, data_object)
        else:
            self.buffer.refresh(ticker)

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
            data = None
            print("[WARN] No valid company data found for " + ticker)

        return data
