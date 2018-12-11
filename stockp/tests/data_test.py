import unittest
from bs4 import BeautifulSoup
from stockp import data


class TestData(unittest.TestCase):
    def test_fetcher(self):
        tree = data.Fetcher('stockp/tests/stubs.html')()
        self.assertIsInstance(tree, BeautifulSoup)

    def test_stock(self):
        stock = data.Stock('Dec 11, 2018', '16.32', '16.42', '16.299999', '16.32', '16.32', '15,800')
        self.assertEqual(str(stock), "Stock('2018-12-11', 16.32, 16.42, 16.30, 16.32, 16.32, 15800)")


if __name__ == '__main__':
    unittest.main()
