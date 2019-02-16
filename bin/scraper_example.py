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

    print('\nTickerData object:')
    print(data)

    # this is a CompanyData object
    data = el.get_company_data(ticker)

    print('\nCompanyData object:')
    print(data)
