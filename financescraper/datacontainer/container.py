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
    def __str__(self):  # pragma: no cover
        pass

    @abstractmethod
    def __repr__(self):  # pragma: no cover
        pass

    @abstractmethod
    def merge(self, other):  # pragma: no cover
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
        return 'TickerData({currency}, {etf}, {name}, {price}, {source})'.format(
            currency=self.currency, etf=self.etf, name=self.name, price=self.price, source=self.source)

    def __str__(self):
        return '{name}: {price:.2f} {currency} from {source} || ETF: {etf}'.format(
            name=self.name, price=self.price, currency=self.currency, source=self.source, etf=self.etf)

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
        return 'CompanyData({description}, {exchange}, {industry}, {name}, {sector}, {source}, {symbol}, {website})' \
            .format(description=self.description, exchange=self.exchange, industry=self.industry, name=self.name,
                    sector=self.sector, source=self.source, symbol=self.symbol, website=self.website)

    def __str__(self):
        return '{symbol}: {name} - {website} from {source} || sector: {sector} || industry: {industry} || exchange: ' \
               '{exchange} || description: {description}'.format(
                symbol=self.symbol, name=self.name, website=self.website, source=self.source, sector=self.sector,
                industry=self.industry, exchange=self.exchange, description=self.description)

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
