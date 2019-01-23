from sample import yahoo_scraper

ticker = ['TSLA', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'AAPL', 'TSLA', 'FZM.F', '7974.T', 'AAPL']

for t in ticker:
    print(yahoo_scraper.get_data(t))
    print(yahoo_scraper.get_company_data(t))
