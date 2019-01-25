import requests
from ..core import scraper
import json


class CurrencyConverter:
    def __init__(self, target_currency_code):
        self.target_currency_code = target_currency_code
        self.yahoo_scraper = scraper.YahooScraper(False)

    def convert(self, base_currency_code, amount):
        exchange_rate = self._get_exchange_rate(base_currency_code, self.target_currency_code)
        if exchange_rate is None:
            return exchange_rate
        else:
            return amount * exchange_rate

    def _get_exchange_rate(self, base_curr, dest_curr):
        res = self.yahoo_scraper.session.get(self.yahoo_scraper.url + base_curr + dest_curr + "=X")
        if not (res.status_code == requests.codes.ok):
            print('[ERR] data fetching failed')
            return None

        raw_data = res.text

        object_start = raw_data.find("root.App.main") + 16
        object_end = raw_data.find("</script>", object_start) - 12
        data_json = raw_data[object_start: object_end]

        data_object = json.loads(data_json)
        rate = None
        try:
            rate = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']
        except KeyError:
            print("[ERR] No valid conversion data found for " + base_curr + " to " + dest_curr)

        return rate
