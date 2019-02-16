import copy

from abc import ABC, abstractmethod


class DataObject(ABC):
    __slots__ = ('name', 'source')

    def __init__(self, source):
        self.source = source
        self.name = 'No name found'

    def __eq__(self, other):
        equality = True
        for prop in self.__slots__:
            equality = equality and (getattr(self, prop) == getattr(other, prop))
        for prop in DataObject.__slots__:
            equality = equality and (getattr(self, prop) == getattr(other, prop))
        return equality

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def merge(self, other):
        pass


class TickerData(DataObject):
    __slots__ = (
        'currency',
        'etf',
        'price',
    )

    def __init__(self, source):
        super().__init__(source)
        self.currency = 'USD'
        self.etf = False
        self.price = 0.0

    def __repr__(self):
        return 'TickerData(%s, %r, %s, %f, %s)' % (self.currency, self.etf, self.name, self.price, self.source)

    def __str__(self):
        return '%s: %f %s from %s || ETF: %r' % (self.name, self.price, self.currency, self.source, self.etf)

    # merge the other TickerData object into self and return self
    def merge(self, other):
        pre_merge = copy.copy(self)
        new_price_and_curr = other.currency != 'USD' and self.currency != other.currency
        if new_price_and_curr:
            self.currency = other.currency
            self.price = other.price
        self.etf = self.etf and other.etf
        self.name = other.name if self.name == 'No name found' else self.name
        if not pre_merge == self:
            self.source = self.source + ' & ' + other.source
        return self


class CompanyData(DataObject):
    __slots__ = (
        'description',
        'exchange',
        'industry',
        'sector',
        'symbol',
        'website'
    )

    def __init__(self, source):
        super().__init__(source)
        self.description = 'No description found'
        self.exchange = 'No exchange found'
        self.industry = 'No industry found'
        self.sector = 'No sector found'
        self.symbol = ''
        self.website = 'No website found'

    def __repr__(self):
        return 'CompanyData(%s, %s, %s, %s, %s, %s, %s, %s)' % (self.description, self.exchange, self.industry,
                                                                self.name, self.sector, self.source, self.symbol,
                                                                self.website)

    def __str__(self):
        return '%s: %s - %s from %s || sector: %s || industry %s || exchange: %s || description: %s' % \
               (self.symbol, self.name, self.website, self.source, self.sector, self.industry, self.exchange,
                self.description)

    # merge the other TickerData object into self and return self
    def merge(self, other):
        pre_merge = copy.copy(self)
        for prop in self.__slots__:
            new_val = getattr(other, prop) if getattr(self, prop) == 'No ' + prop + ' found' else getattr(self, prop)
            setattr(self, prop, new_val)
        for prop in DataObject.__slots__:
            new_val = getattr(other, prop) if getattr(self, prop) == 'No ' + prop + ' found' else getattr(self, prop)
            setattr(self, prop, new_val)
        if not pre_merge == self:
            self.source = self.source + ' & ' + other.source
        return self
