import financescraper

ticker = ['TSLA', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'AAPL', 'TSLA', 'FZM.F', '7974.T', 'AAPL']
currencies = ['USD', 'EUR', 'GBP', 'JPY', 'USD', 'EUR']

dollar_converter = financescraper.conversions.CurrencyConverter('USD')
euro_converter = financescraper.conversions.CurrencyConverter('EUR')
yahoo_scraper = financescraper.scraper.YahooScraper()

for t in ticker:
    print(yahoo_scraper.get_data(t))
    print(yahoo_scraper.get_company_data(t))

for c in currencies:
    print(dollar_converter.convert(c, 1))
    print(euro_converter.convert(c, 1))
