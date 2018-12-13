from json import dumps
from os import environ
from stockp.data import Downloader, Parser


class Forecaster:
    """
    Synopsis
    ========
    Computes the forecast of stocks by computing the mean of last specified 
    closing prices.
    
    Examples
    ========
    >>> forecaster = Forecaster((16.52, 16.42, '16.22'), limit=2)
    >>> forecaster()
    16.47
    """

    LIMIT = 3

    def __init__(self, entities, limit=LIMIT):
        self.entities = entities
        self.limit = float(limit)

    @property
    def data(self):
        data = []
        for i, e in enumerate(self.entities):
            if i == self.limit:
                break
            data.append(float(e))
        return data

    def __call__(self):
        return sum(self.data) / self.limit 


class Global:
    """
    Synopsis
    ========
    A data object aimed to be used as a global configuration (instantiated once)
    and avoid downloading and fetching on each server request.
    Can be iterated to fetch a tuple of properties.
    """

    __instance = None

    COLORS = ('green', 'red', 'blue')
    LABELS = ('corn', 'gasoline', 'nasdaq')

    def __init__(self, downloader=Downloader, parser=Parser, forecaster=Forecaster):
        self.downloader = downloader
        self.parser = parser
        self.forecaster = forecaster
        self.stocks = self._stocks()
        self.forecasts = self._forecasts()

    def __iter__(self):
        return (e for e in (self.parser.LIMIT, zip(self.COLORS, self._prices()), zip(self.LABELS, self.forecasts)))

    def _prices(self):
        return (dumps([float(e) for e in entities]) for entities in self.stocks)

    def _stocks(self):
        return [list(self.parser(tree)) for tree in self.downloader()]

    def _forecasts(self):
        return [self.forecaster(entities)() for entities in self.stocks]


GLOBAL = Global()
