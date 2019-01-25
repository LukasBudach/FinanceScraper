from sample import scraper

ticker = ['TSLA', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'AAPL', 'TSLA', 'FZM.F', '7974.T', 'AAPL']
yahoo_scraper = scraper.YahooScraper()

for t in ticker:
    print(yahoo_scraper.get_data(t))
    print(yahoo_scraper.get_company_data(t))
