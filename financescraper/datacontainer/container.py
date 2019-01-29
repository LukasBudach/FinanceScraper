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
