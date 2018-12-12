import unittest
from stockp import computer


class TestComputer(unittest.TestCase):
    def test_forecaster(self):
        data = (v for v in (16.52, 16.42, '16.22', 1000))
        forecaster = computer.Forecaster(data)
        mean = forecaster()
        self.assertEqual(mean, 16.386666666666667)


if __name__ == '__main__':
    unittest.main()
