from concurrent.futures import ThreadPoolExecutor
from os import path
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from stockp.logger import BASE as logger
from stockp.entity import Stock


class Fetcher:
    """
    Synopsis
    ========
    Fetches the specified HTML source locally if present. If it does not exist tries 
    to fetch it remotely from the specified URL. 
    Returns a raw BeautifulSoup object for further parsing.

    Examples
    ========
    >>> fetcher = Fetcher()
    >>> fetcher('stockp/tests/stubs.html').__class__
    <class 'bs4.BeautifulSoup'>
    """

    def __call__(self, doc, url=None):
        doc = path.abspath(doc)
        url = urlparse(url).geturl()
        if not path.exists(doc):
            logger.info('fetching data remotely from %s', url)
            with urlopen(url) as remote, open(doc, 'wb') as local:
                local.write(remote.read())
        with open(doc) as doc:
            return BeautifulSoup(doc, 'html.parser')


class Downloader:
    """
    Synopsis
    ========
    Fetch multiple HTML documents by relying on multi-threading non blocking I/O.
    Accepts a list of URLs, from which to extract document name and can be
    iterated by executing the specified callable in parallel (via threads).

    Examples
    ========
    >>> action = lambda doc, _: doc.split('/')[-1]
    >>> downloader = Downloader(action=action)
    >>> list(downloader)
    ['corn.html', 'uga.html', 'ndaq.html']
    """

    URLS = ('https://finance.yahoo.com/quote/CORN/history?p=CORN', 'https://finance.yahoo.com/quote/UGA/history?p=UGA', 'https://finance.yahoo.com/quote/NDAQ/history?p=NDAQ')
    PATH = 'cache/'
    EXT = 'html'

    def __init__(self, urls=URLS, _path=PATH, action=Fetcher()):
        self.urls = tuple(urls) 
        self.docs = tuple(self._doc(url, _path) for url in urls)
        self.workers = len(self.urls)
        self.action = action

    def __iter__(self):
         with ThreadPoolExecutor(max_workers=self.workers) as executor:
             for doc, url in zip(self.docs, self.urls):
                 future = executor.submit(self.action, doc, url)
                 yield future.result()

    def _doc(self, url, _path):
        name = str(url).split('=')[-1].lower()
        name = '%s.%s' % (name, self.EXT)
        return path.abspath(path.join(_path, name))


class Parser:
    """
    Synopsis
    ========
    Receive an BeautifulSoup object containing the stock prices in USD.
    The instance can be iterated over a (limited) enumerable of specified 
    entity objects.

    Examples
    ========
    >>> html = '<tbody data-reactid="48"><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="49"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="50"><span data-reactid="51">Dec 11, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="52"><span data-reactid="53">16.4100</span></td><td class="Py(10px) Pstart(10px)" data-reactid="54"><span data-reactid="55">16.4300</span></td><td class="Py(10px) Pstart(10px)" data-reactid="56"><span data-reactid="57">16.3652</span></td><td class="Py(10px) Pstart(10px)" data-reactid="58"><span data-reactid="59">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="60"><span data-reactid="61">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="62"><span data-reactid="63">8,676</span></td></tr><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="64"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="65"><span data-reactid="66">Dec 10, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="67"><span data-reactid="68">16.3700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="69"><span data-reactid="70">16.4700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="71"><span data-reactid="72">16.3600</span></td><td class="Py(10px) Pstart(10px)" data-reactid="73"><span data-reactid="74">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="75"><span data-reactid="76">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="77"><span data-reactid="78">25,800</span></td></tr><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="79"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="80"><span data-reactid="81">Dec 07, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="82"><span data-reactid="83">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="84"><span data-reactid="85">16.4700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="86"><span data-reactid="87">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="88"><span data-reactid="89">16.4500</span></td><td class="Py(10px) Pstart(10px)" data-reactid="90"><span data-reactid="91">16.4500</span></td><td class="Py(10px) Pstart(10px)" data-reactid="92"><span data-reactid="93">124,200</span></td></tr></tbody>'
    >>> tree = BeautifulSoup(html, 'html.parser')
    >>> parser = Parser(tree, limit=2)
    >>> list(parser)
    [Stock('2018-12-11', 16.41, 16.43, 16.37, 16.40, 16.40, 8676), Stock('2018-12-10', 16.37, 16.47, 16.36, 16.38, 16.38, 25800)]
    """

    LIMIT = 30

    def __init__(self, tree, entity=Stock, limit=LIMIT):
        self.tree = tree
        self.limit = int(limit)
        self.entity = entity

    def __iter__(self):
        count = 0
        for row in self.tree.tbody.find_all('tr'):
            if count == self.limit:
                break
            cells = row.find_all('td')
            data = tuple(cell.get_text() for cell in cells)
            try:
                yield self.entity(*data)
                count += 1
            except ValueError as e:
                logger.error('parsed data error on %r: %s', data, e)
