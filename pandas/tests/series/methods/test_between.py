import numpy as np

from pandas import (
    Series,
    bdate_range,
    date_range,
    period_range,
)
import pandas._testing as tm


class TestBetween:

    # TODO: redundant with test_between_datetime_values?
    def test_between(self):
        series = Series(date_range("1/1/2000", periods=10))
        left, right = series[[2, 7]]

        result = series.between(left, right)
        expected = (series >= left) & (series <= right)
        tm.assert_series_equal(result, expected)

    def test_between_datetime_values(self):
        ser = Series(bdate_range("1/1/2000", periods=20).astype(object))
        ser[::2] = np.nan

        result = ser[ser.between(ser[3], ser[17])]
        expected = ser[3:18].dropna()
        tm.assert_series_equal(result, expected)

        result = ser[ser.between(ser[3], ser[17], inclusive=False)]
        expected = ser[5:16].dropna()
        tm.assert_series_equal(result, expected)

    def test_between_period_values(self):
        ser = Series(period_range("2000-01-01", periods=10, freq="D"))
        left, right = ser[[2, 7]]
        result = ser.between(left, right)
        expected = (ser >= left) & (ser <= right)
        tm.assert_series_equal(result, expected)

    def test_inclusive(self):
        ser = Series([1, 2, 3, 4, 5, 6, 7, 8])
        left = 2
        right = 5

        result = ser.between(left, right)
        expected = (ser >= left) & (ser <= right)
        tm.assert_almost_equal(result, expected)

        result = ser.between(left, right, inclusive=(True, True))
        expected = (ser >= left) & (ser <= right)
        tm.assert_almost_equal(result, expected)

        result = ser.between(left, right, inclusive=False)
        expected = (ser > left) & (ser < right)
        tm.assert_almost_equal(result, expected)

        result = ser.between(left, right, inclusive=(False, False))
        expected = (ser > left) & (ser < right)
        tm.assert_almost_equal(result, expected)

        result = ser.between(left, right, inclusive=(True, False))
        expected = (ser >= left) & (ser < right)
        tm.assert_almost_equal(result, expected)

        result = ser.between(left, right, inclusive="left")
        expected = (ser >= left) & (ser < right)
        tm.assert_almost_equal(result, expected)

        result = ser.between(left, right, inclusive="right")
        expected = (ser > left) & (ser <= right)
        tm.assert_almost_equal(result, expected)
