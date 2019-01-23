import urllib.request
import json


def _get_exchange_rate(base_curr, dest_curr):
    req = urllib.request.urlopen("https://finance.yahoo.com/quote/" + base_curr + dest_curr +"=X")
    html_bytes = req.read()

    html_string = html_bytes.decode("utf8")
    req.close()

    object_start = html_string.find("root.App.main") + 16
    object_end = html_string.find("</script>", object_start) - 12

    html_string_cut = html_string[object_start: object_end]

    data_object = json.loads(html_string_cut)
    rate = 1
    try:
        rate = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']
    except KeyError:
        print("[WARN] No valid conversion data found for " + base_curr + " to " + dest_curr +
                        ". Using 1:1 conversion.")

    return rate


def to_usd(amount, base_currency_symbol):
    if base_currency_symbol == '€':
        return amount * _get_exchange_rate('EUR', 'USD')
    elif base_currency_symbol == '¥':
        return amount * _get_exchange_rate('JPY', 'USD')
    # expandable for a lot of different currencies
    else:
        print("[WARN] Requested conversion from unknown currency symbol " + base_currency_symbol +
                        " to USD. Using 1:1 conversion.")
    return amount