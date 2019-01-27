from financescraper import scraper

yahoo_scraper = scraper.YahooScraper()

print(yahoo_scraper.get_data('AMZN'))
print(yahoo_scraper.get_company_data('AMZN'))
