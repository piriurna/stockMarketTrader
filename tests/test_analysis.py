import unittest
import pandas as pd
import math
from analysis import (
    calculate_moving_average,
    calculate_return,
)


class TestStockAnalysis(unittest.TestCase):
    def setUp(self):
        data = {'4. close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
        self.stock_data = pd.DataFrame(data)

    def test_calculate_moving_average(self):
        result = calculate_moving_average(self.stock_data['4. close'], 3)
        expected = [math.nan, math.nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        for r, e in zip(result, expected):
            if math.isnan(e):
                self.assertTrue(math.isnan(r))
            else:
                self.assertAlmostEqual(r, e, places=6)

    def test_calculate_return(self):
        result = calculate_return(self.stock_data['4. close'])
        expected = [math.nan, 1.0, 0.5, 0.3333333333333333, 0.25, 0.2, 0.16666666666666666, 0.14285714285714285,
                    0.125, 0.1111111111111111]
        for r, e in zip(result, expected):
            if math.isnan(e):
                self.assertTrue(math.isnan(r))
            else:
                self.assertAlmostEqual(r, e, places=6)


if __name__ == '__main__':
    unittest.main()
