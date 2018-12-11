from datetime import datetime
from os import path
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from stockp.logger import BASE as logger


class Fetcher:
    """
    Synopsis
    ========
    Fetches the specified HTML source locally if present. If it does not exist tries 
    to fetch it remotely from the specified URL. 
    Returns a raw BeautifulSoup object for further parsing.

    Examples
    ========
    >>> fetcher = Fetcher('stockp/tests/stubs.html')
    >>> fetcher().__class__
    <class 'bs4.BeautifulSoup'>
    """

    def __init__(self, doc, url=None):
        self.doc = path.abspath(doc)
        self.url = urlparse(url).geturl()

    def __call__(self):
        if not path.exists(self.doc):
            logger.info('fetching data remotely from %s', self.url)
            with urlopen(self.url) as remote, open(self.doc, 'wb') as local:
                local.write(remote.read())
        with open(self.doc) as doc:
            return BeautifulSoup(doc, 'html.parser')


class Parser:
    """
    Synopsis
    ========
    Receive an BeautifulSoup object containing the stock prices in USD and
    can be iterated as a list of the last month stock rates (or by specified limit).

    Examples
    ========
    >>> html = '<tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="49"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="50"><span data-reactid="51">Dec 11, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="52"><span data-reactid="53">16.4100</span></td><td class="Py(10px) Pstart(10px)" data-reactid="54"><span data-reactid="55">16.4300</span></td><td class="Py(10px) Pstart(10px)" data-reactid="56"><span data-reactid="57">16.3652</span></td><td class="Py(10px) Pstart(10px)" data-reactid="58"><span data-reactid="59">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="60"><span data-reactid="61">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="62"><span data-reactid="63">8,676</span></td></tr><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="64"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="65"><span data-reactid="66">Dec 10, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="67"><span data-reactid="68">16.3700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="69"><span data-reactid="70">16.4700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="71"><span data-reactid="72">16.3600</span></td><td class="Py(10px) Pstart(10px)" data-reactid="73"><span data-reactid="74">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="75"><span data-reactid="76">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="77"><span data-reactid="78">25,800</span></td></tr><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="79"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="80"><span data-reactid="81">Dec 07, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="82"><span data-reactid="83">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="84"><span data-reactid="85">16.4700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="86"><span data-reactid="87">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="88"><span data-reactid="89">16.4500</span></td><td class="Py(10px) Pstart(10px)" data-reactid="90"><span data-reactid="91">16.4500</span></td><td class="Py(10px) Pstart(10px)" data-reactid="92"><span data-reactid="93">124,200</span></td></tr>'
    >>> data = BeautifulSoup(html, 'html.parser')
    >>> parser = Parser(data, limit=2)
    >>> list(parser)
    []
    
    [('Dec 11, 2018', '16.4100', '16.4300', '16.3652', '16.4000', '16.4000', '8,676'), ('Dec 10, 2018', '16.3700', '16.4700', '16.3600', '16.3800', '16.3800', '25,800)]
    """

    LIMIT = 30

    def __init__(self, data, limit=LIMIT):
        self.data = data
        self.limit = int(limit)

    def __iter__(self):
        return iter([])


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

    def __repr__(self):
        data = (self.__class__.__name__, ) + tuple(self)
        return "%s('%s', %.2f, %.2f, %.2f, %.2f, %.2f, %d)" % data

    def __iter__(self):
        return (getattr(self, attr) for attr in self.__slots__)

    def _int(self, n):
        n = str(n).replace(',', '')
        return int(n)
