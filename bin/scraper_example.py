from financescraper import scraper

# creates the scraper object with its default arguments (see documentation)
yahoo_scraper = scraper.YahooScraper()
ticker = 'AMZN'

# this is a TickerData object
data = yahoo_scraper.get_data(ticker)

print('\nFields of TickerData object:')
print('Currency: ' + data.currency)
print('is ETF:', data.etf)
print('Name: ' + data.name)
print('Price:', data.price)
print('Source: ' + data.source)

# this is a CompanyData object
data = yahoo_scraper.get_company_data(ticker)

print('\nFields of CompanyData object:')
print('Description: ' + data.description)
print('Exchange: ' + data.exchange)
print('Industry: ' + data.industry)
print('Name: ' + data.name)
print('Sector: ' + data.sector)
print('Symbol: ' + data.symbol)
print('Website: ' + data.website)
