from financescraper import scraper

# creates the scraper object with its default arguments (see documentation)
yahoo_scraper = scraper.YahooScraper()
iex_scraper = scraper.IEXScraper()
general_scraper = scraper.FinanceScraper()
scraper = [yahoo_scraper, iex_scraper, general_scraper]
ticker = 'AMZN'

# this is a TickerData object
for el in scraper:
    data = el.get_data(ticker)

    print('\nFields of TickerData object:')
    print('Currency: ' + data.currency)
    print('is ETF:', data.etf)
    print('Name: ' + data.name)
    print('Price:', data.price)
    print('Source: ' + data.source)

    # this is a CompanyData object
    data = el.get_company_data(ticker)

    print('\nFields of CompanyData object:')
    print('Description: ' + data.description)
    print('Exchange: ' + data.exchange)
    print('Industry: ' + data.industry)
    print('Name: ' + data.name)
    print('Sector: ' + data.sector)
    print('Source: ' + data.source)
    print('Symbol: ' + data.symbol)
    print('Website: ' + data.website)
