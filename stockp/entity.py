from datetime import datetime
from json import dumps


class Stock:
    """
    Synopsis
    ========
    Represents the stock data value object. 
    Attributes are properly casted to the right type directly on constructor.
    
    Examples
    ========
    >>> plain = Stock('Oct 29, 2018')
    >>> print(plain)
    Stock('2018-10-29', 0.00, 0.00, 0.00, 0.00, 0.00, 0)

    >>> stock = Stock('Dec 11, 2018', '16.32', '16.42', '16.299999', '16.32', '16.32', '15,800')
    >>> print(stock)
    Stock('2018-12-11', 16.32, 16.42, 16.30, 16.32, 16.32, 15800)
    """

    FORMAT = '%b %d, %Y'

    __slots__ = ('date', '_open', 'high', 'low', 'close', 'adj', 'volume')

    def __init__(self, date, _open=.0, high=.0, low=.0, 
                 close=.0, adj=.0, volume=0):
        self.date = datetime.strptime(date, self.FORMAT).date()
        self._open = float(_open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.adj = float(adj)
        self.volume = self._int(volume)

    @property
    def payload(self):
        payload = {k.replace('_', ''): v for k, v in zip(self.__slots__, iter(self))}
        return dumps(payload, default=str)

    def __repr__(self):
        data = (self.__class__.__name__, ) + tuple(self)
        return "%s('%s', %.2f, %.2f, %.2f, %.2f, %.2f, %d)" % data

    def __iter__(self):
        return (getattr(self, attr) for attr in self.__slots__)

    def __float__(self):
        return self.close

    def _int(self, n):
        n = str(n).replace(',', '')
        return int(n)
