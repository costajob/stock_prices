import unittest
from stockp import entity


class TestEntity(unittest.TestCase):
    def test_stock(self):
        stock = entity.Stock('Dec 11, 2018', '16.32', '16.42', '16.299999', '16.32', '16.32', '15,800')
        self.assertEqual(str(stock), "Stock('2018-12-11', 16.32, 16.42, 16.30, 16.32, 16.32, 15800)")
        self.assertEqual(float(stock), 16.32)
        self.assertEqual(stock.payload, '{"date": "2018-12-11", "open": 16.32, "high": 16.42, "low": 16.299999, "close": 16.32, "adj": 16.32, "volume": 15800}')


if __name__ == '__main__':
    unittest.main()
