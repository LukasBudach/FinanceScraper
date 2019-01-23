import urllib.request
import json


def get_data(ticker):
    return _get_data_from_yahoo(ticker)


def _get_data_from_yahoo(ticker):
    data = None

    req = urllib.request.urlopen("https://finance.yahoo.com/quote/" + ticker)
    html_bytes = req.read()

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
    req = urllib.request.urlopen("https://finance.yahoo.com/quote/" + ticker)
    html_bytes = req.read()

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
