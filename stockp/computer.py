from statistics import mean


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
        self.limit = int(limit)

    @property
    def data(self):
        data = []
        for i, e in enumerate(self.entities):
            if i == self.limit:
                break
            data.append(float(e))
        return data

    def __call__(self):
        return mean(self.data)
