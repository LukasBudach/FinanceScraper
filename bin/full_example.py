import financescraper
import time

# say you want to get the data to the following tickers in the listed order:
ticker = ['TSLA', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'TL0.F', 'FZM.F', '7974.T', 'AAPL', 'SPY']

# you explicitly want to use finance.yahoo.com as your source
# creates the scraper object with its default arguments (can be seen in documentation)
yahoo_scraper = financescraper.scraper.YahooScraper()
iex_scraper = financescraper.scraper.IEXScraper()
general_scraper = financescraper.scraper.FinanceScraper()

scraper = [yahoo_scraper, iex_scraper, general_scraper]

# you also want to convert the price to USD and EUR
dollar_converter = financescraper.conversions.CurrencyConverter('USD')
euro_converter = financescraper.conversions.CurrencyConverter('EUR')

file = open('output.txt', 'w+')

for s in scraper:
    file.write('-----------------------------------------\n')
    file.write(str(type(s)) + '\n')
    total_time = 0
    for t in ticker:
        # stop how long one process takes to see the buffer in action
        start_time = time.time_ns()

        # probably want some feedback when stuff is written, because fetching the data takes a bit
        print("Fetching and writing %s" % t)

        # you get the ticker data containing essential information like name associated with the ticker, quote and price
        ticker_data = s.get_data(t)

        # also want to get some information on the company behind the ticker like exchange, website, industry and sector
        company_data = s.get_company_data(t)

        end_time = time.time_ns()

        total_time = total_time + (end_time - start_time)

        if ticker_data is not None:
            file.write("\nSource: %s -- Fetch time: %f ms \n%s : %f USD -- %f EUR -- Is ETF: %r \n"
                       % (ticker_data.source, (end_time-start_time)/1000000,
                          ticker_data.name,
                          dollar_converter.convert(ticker_data.currency, ticker_data.price),
                          euro_converter.convert(ticker_data.currency, ticker_data.price),
                          ticker_data.etf)
                       )

        if company_data is not None:
            file.write("Exchange: %s -- Industry: %s -- Sector: %s -- Website: %s \n"
                       % (company_data.exchange, company_data.industry, company_data.sector, company_data.website)
                       )
    file.write('\n total time needed: %f' % (total_time/1000000))
    file.write('\n-----------------------------------------\n')

file.close()

# you can now check out all of the data written in output.txt in this directory
print('Done writing to output.txt')
