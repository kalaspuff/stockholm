from typing import Any, Optional

import pytest

from stockholm import Money, CurrencyMismatchError, ConversionError


@pytest.mark.parametrize(
    "values, expected, exception_expected",
    [
        ([1, 2, 3, 4], 10, None),
        ([1, -1, 2, -2, 10, 4711, 1338, -10000], -3941, None),
        (["23.50 SEK", "50.00 SEK", "91.21 SEK", "9053 SEK", 20], Money("9237.71", currency="SEK"), None),
        ([Money(100, currency="EUR"), 20, "1.5000", "-0.008 EUR", 1.10], Money("122.592", currency="EUR"), None),
        (["1 EUR", "1 SEK"], None, CurrencyMismatchError),
        (["0 EUR", "0 SEK"], None, CurrencyMismatchError),
        (["0 EUR", "0 EUR"], "0 EUR", None),
        (["1 EUR", "1 EUR"], "2.00 EUR", None),
        (["3.14", "3.14", "3.14", "ABC"], None, ConversionError),
    ],
)
def test_sum_list(values: Any, expected: Any, exception_expected: Optional[Exception]) -> None:
    try:
        m = Money.sum(values)
        if exception_expected:
            assert False, "Exception expected"
        assert isinstance(m, Money)
        assert m == expected
    except Exception as ex:
        if not exception_expected:
            raise
        if not isinstance(ex, exception_expected):
            raise

    assert True


def test_sum_list_cent_values() -> None:
    values = [471100, 10000, 509000, 350200, "313450", "900400", "1000", "100", 13999]
    m = Money.sum(values, currency="SEK", is_cents=True)

    assert isinstance(m, Money)
    assert m == Money(2569249, currency="SEK", is_cents=True)
    assert m == Money("25692.49 SEK")
    assert str(m) == "25692.49 SEK"
