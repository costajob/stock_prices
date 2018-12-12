import unittest
from bs4 import BeautifulSoup
from stockp import data


class TestData(unittest.TestCase):
    def test_stock(self):
        stock = data.Stock('Dec 11, 2018', '16.32', '16.42', '16.299999', '16.32', '16.32', '15,800')
        self.assertEqual(str(stock), "Stock('2018-12-11', 16.32, 16.42, 16.30, 16.32, 16.32, 15800)")

    def test_fetcher(self):
        fetcher = data.Fetcher()
        tree = fetcher('stockp/tests/stubs.html')
        self.assertIsInstance(tree, BeautifulSoup)

    def test_downloader(self):
        action = lambda doc, _: doc.split('/')[-1]
        downloader = data.Downloader(action=action)
        docs = list(downloader)
        self.assertEqual(docs, ['corn.html', 'uga.html', 'ndaq.html'])

    def test_parser(self):
        html = '<tbody data-reactid="48"><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="49"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="50"><span data-reactid="51">Dec 11, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="52"><span data-reactid="53">16.4100</span></td><td class="Py(10px) Pstart(10px)" data-reactid="54"><span data-reactid="55">16.4300</span></td><td class="Py(10px) Pstart(10px)" data-reactid="56"><span data-reactid="57">16.3652</span></td><td class="Py(10px) Pstart(10px)" data-reactid="58"><span data-reactid="59">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="60"><span data-reactid="61">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="62"><span data-reactid="63">8,676</span></td></tr><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="64"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="65"><span data-reactid="66">Dec 10, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="67"><span data-reactid="68">16.3700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="69"><span data-reactid="70">16.4700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="71"><span data-reactid="72">16.3600</span></td><td class="Py(10px) Pstart(10px)" data-reactid="73"><span data-reactid="74">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="75"><span data-reactid="76">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="77"><span data-reactid="78">25,800</span></td></tr><tr class="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)" data-reactid="79"><td class="Py(10px) Ta(start) Pend(10px)" data-reactid="80"><span data-reactid="81">Dec 07, 2018</span></td><td class="Py(10px) Pstart(10px)" data-reactid="82"><span data-reactid="83">16.4000</span></td><td class="Py(10px) Pstart(10px)" data-reactid="84"><span data-reactid="85">16.4700</span></td><td class="Py(10px) Pstart(10px)" data-reactid="86"><span data-reactid="87">16.3800</span></td><td class="Py(10px) Pstart(10px)" data-reactid="88"><span data-reactid="89">16.4500</span></td><td class="Py(10px) Pstart(10px)" data-reactid="90"><span data-reactid="91">16.4500</span></td><td class="Py(10px) Pstart(10px)" data-reactid="92"><span data-reactid="93">124,200</span></td></tr></tbody>'
        tree = BeautifulSoup(html, 'html.parser')
        parser = data.Parser(tree, limit=2)
        for stock in parser:
            self.assertIsInstance(stock, data.Stock)


if __name__ == '__main__':
    unittest.main()
