from financescraper.core import conversions

# creates converter object with its default arguments (see documentation)
usd_converter = conversions.CurrencyConverter('USD')

print('\nConvert 100 EUR to USD:')
print(usd_converter.convert('EUR', 100))
print('\nConvert 100 JPY to USD:')
print(usd_converter.convert('JPY', 100))
print('\nConvert 100 USD to USD:')
print(usd_converter.convert('USD', 100))
