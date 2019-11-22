import pytest

from stockholm import Money


@pytest.mark.parametrize("amount, currency, is_cents, expected", [
    ("0", None, False, "0.00"),
    ("1", None, False, "1.00"),
    ("1.1", None, False, "1.10"),
    ("1.51", None, False, "1.51"),
    (0, None, True, "0.00"),
    (1, None, True, "0.01"),
    (100, None, True, "1.00"),
    (4711, None, True, "47.11"),
    (23.52, None, True, "0.2352"),
    ("100", None, True, "1.00"),
    ("23.52", None, True, "0.2352"),
    (0, None, False, "0.00"),
    (1.0, None, False, "1.00"),
    (1.1, None, False, "1.10"),
    (1.51, None, False, "1.51"),
    (3.14, None, False, "3.14"),
    (3.141592653, None, False, "3.141592653"),
    (3.1415926535, None, False, "3.141592654"),
    (1.51100000, None, False, "1.511"),
    (2.4000000000000004, None, False, "2.40"),
    ("1.5100", None, False, "1.51"),
    ("1.0000", None, False, "1.00"),
    ("1.1001", None, False, "1.1001"),
    ("1.100100", None, False, "1.1001"),
    ("0", "SEK", False, "0.00 SEK"),
    (0, "SEK", False, "0.00 SEK"),
    (0.0, "SEK", False, "0.00 SEK"),
    ("4711", "EUR", False, "4711.00 EUR"),
    ("4711", "EUR", False, "4711.00 EUR"),
    ("4711", "EUR", False, "4711.00 EUR"),
    ("1 EUR", None, False, "1.00 EUR"),
    ("1 EUR", "EUR", False, "1.00 EUR"),
    ("3.14 DKK", None, False, "3.14 DKK"),
    ("3.14 DKK", "DKK", False, "3.14 DKK"),
    ("3.1415 DKK", None, False, "3.1415 DKK"),
    ("3.1415", "DKK", False, "3.1415 DKK"),
    ("4711 EUR", "EUR", False, "4711.00 EUR"),
    ("0 EUR", None, False, "0.00 EUR"),
    ("EUR 0", None, False, "0.00 EUR"),
    ("SEK 1338", None, False, "1338.00 SEK"),
    ("USD 13.38", None, False, "13.38 USD"),
    ("4711.999101000", "USD", False, "4711.999101 USD"),
    ("-0", None, False, "0.00"),
    (-0, None, False, "0.00"),
])
def test_basic_str_output(amount, currency, is_cents, expected):
    m = Money(amount, currency=currency, is_cents=is_cents)
    assert str(m) == expected
