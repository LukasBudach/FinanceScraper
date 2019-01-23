import requests
import json


class YahooScraper:
    def __init__(self):
        self.session = requests.Session()
        self.url = 'https://finance.yahoo.com/quote/'
        self.session.get('https://finance.yahoo.com')

    def get_data(self, ticker):
        return _format_data(self.session.get(self.url + ticker))


def _format_data(raw, source, ticker):
    if not (raw.status_code == requests.codes.ok):
        print('[ERR] data fetching failed')
        return

    bulk_data = raw.text

    object_start = bulk_data.find("root.App.main") + 16
    object_end = bulk_data.find("</script>", object_start) - 12

    data = bulk_data[object_start: object_end]

    data_object = json.loads(data)

    data_dict = {}

    try:
        quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
        data_dict['Source'] = 'Yahoo'
        data_dict['Price'] = quote_summary['financialData']['currentPrice']['raw']
        data_dict['Currency'] = quote_summary['price']['currency']
        data_dict['Security Name'] = quote_summary['price']['longName']
        data_dict['ETF'] = (quote_summary['price']['quoteType'] == 'ETF')
        data_dict['Valid'] = True;
    except KeyError:
        print("[WARN] No valid data found for " + ticker)

    return data_dict


def _get_data_from_yahoo(ticker):
    data = None

    req = requests.get("https://finance.yahoo.com/quote/" + ticker)
    html_bytes = req.text()

    html_string = html_bytes.decode("utf8")
    req.close()

    object_start = html_string.find("root.App.main") + 16
    object_end = html_string.find("</script>", object_start) - 12

    html_string_cut = html_string[object_start: object_end]

    data_object = json.loads(html_string_cut)

    data_dict = { }

    try:
        quote_summary = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']
        data_dict['Source'] = 'Yahoo'
        data_dict['Price'] = quote_summary['financialData']['currentPrice']['raw']
        data_dict['Currency'] = quote_summary['price']['currency']
        data_dict['Security Name'] = quote_summary['price']['longName']
        data_dict['ETF'] = (quote_summary['price']['quoteType'] == 'ETF')
        data_dict['Valid'] = True;
    except KeyError:
        print("[WARN] No valid data found for " + ticker)

    return data_dict


def _get_company_from_yahoo(ticker):
    req =requests.get("https://finance.yahoo.com/quote/" + ticker)
    html_bytes = req.text()

    html_string = html_bytes.decode("utf8")
    req.close()

    object_start = html_string.find("root.App.main") + 16
    object_end = html_string.find("</script>", object_start) - 12

    html_string_cut = html_string[object_start: object_end]

    data_object = json.loads(html_string_cut)
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
