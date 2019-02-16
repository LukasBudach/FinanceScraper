class TickerData(object):
    __slots__ = (
        'currency',
        'etf',
        'name',
        'price',
        'source'
    )

    def __init__(self, source):
        self.currency = 'USD'
        self.etf = False
        self.name = ''
        self.price = 0.0
        self.source = source

    # merge the other TickerData object into self and return self
    def merge(self, other):
        new_price_and_curr = other.currency != 'USD' and self.currency != other.currency
        if new_price_and_curr:
            self.currency = other.currency
            self.price = other.price
        self.etf = self.etf and other.etf
        self.name = other.name if self.name == '' else self.name
        if not self == self:
            self.source = self.source + ' & ' + other.source
        return self

    def __eq__(self, other):
        equality = True
        equality = equality and (self.currency == other.currency)
        equality = equality and (self.etf == other.etf)
        equality = equality and (self.name == other.name)
        equality = equality and (self.price == other.price)
        equality = equality and (self.source == other.source)
        return equality

class CompanyData(object):
    __slots__ = (
        'description',
        'exchange',
        'industry',
        'name',
        'sector',
        'source',
        'symbol',
        'website'
    )

    def __init__(self, source):
        self.description = ''
        self.exchange = ''
        self.industry = ''
        self.name = ''
        self.sector = ''
        self.source = source
        self.symbol = ''
        self.website = ''
