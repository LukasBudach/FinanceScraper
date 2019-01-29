import financescraper

ticker = ['TSLA', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'AAPL', 'TSLA', 'FZM.F', '7974.T', 'AAPL', 'SPY']
currencies = ['USD', 'EUR', 'GBP', 'JPY', 'USD', 'EUR']

dollar_converter = financescraper.core.conversions.CurrencyConverter('USD')
euro_converter = financescraper.core.conversions.CurrencyConverter('EUR')
yahoo_scraper = financescraper.scraper.YahooScraper()

for t in ticker:
    ticker_data = yahoo_scraper.get_data(t)
    company_data = yahoo_scraper.get_company_data(t)

    if ticker_data is not None:
        print(ticker_data.name, ':', ticker_data.price, ticker_data.currency, 'Source:',
              ticker_data.source, 'ETF:', ticker_data.etf)
    if company_data is not None:
        print(company_data.name, ':', company_data.website, company_data.symbol, company_data.sector)

for c in currencies:
    print(dollar_converter.convert(c, 1))
    print(euro_converter.convert(c, 1))
