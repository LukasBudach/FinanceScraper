from financescraper import conversions

usd_converter = conversions.CurrencyConverter('USD')
print(usd_converter.convert('EUR', 100))