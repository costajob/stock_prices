import unittest
from stockp import data


class TestData(unittest.TestCase):
    def test_stock(self):
        stock = data.Stock('2018-11-12', '16.32', '16.42', '16.299999', '16.32', '16.32', '15800')
        self.assertEqual(str(stock), "Stock('2018-11-12', 16.32, 16.42, 16.30, 16.32, 16.32, 15800)")


if __name__ == '__main__':
    unittest.main()
