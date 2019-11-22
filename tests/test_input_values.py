from typing import Any

from decimal import Decimal
import pytest

from stockholm import Money


@pytest.mark.parametrize(
    "amount, currency, exception_expected",
    [
        (1, None, False),
        ("1", None, False),
        ("1.00", None, False),
        (10000000000, None, False),
        (100000000000000, None, False),
        (1.15, None, False),
        ("1.15", None, False),
        ("1.1500", None, False),
        ("1.15.00", None, True),
        ("1338.31337", None, False),
        ("+1338.31337", None, False),
        ("-1338.31337", None, False),
        ("--1338.31337", None, True),
        ("1338..31337", None, True),
        ("1338.", None, True),
        ("", None, True),
        ("  ", None, True),
        ("10  ", None, False),
        ("-0.00", None, False),
        ("-0.01", None, False),
        ("-.00", None, True),
        ("-.01", None, True),
        ("-00", None, False),
        ("-01", None, False),
        ("00009", None, False),
        (".001", None, False),
        ("-.001", None, False),
        ("-.0", None, False),
        (".0", None, False),
        ("..0", None, True),
        ("3.", None, False),
        ("-3.", None, False),
        (".", None, True),
        ("SEK", None, True),
        ("-SEK", None, True),
        ("-0SEK", None, True),
        ("SEK0", None, True),
        ("SEK-0", None, True),
        ("SEK-0", None, True),
        ("SEK 0", None, False),
        ("SEK 4711.15", None, False),
        ("0 USD", None, False),
        ("4711.15 USD", None, False),
        ("SEK 0 USD", None, True),
        ("SEK 4711.15 USD", None, True),
        (":SEK 0.00", None, True),
        ("1000.4141561 XDR", None, False),
        ("1e5", None, False),
        ("-1e2", None, False),
        ("-1e-2", None, False),
        ("1000 SEK", None, False),
        ("1000 SEK", "SEK", False),
        ("1000 SEK", "USD", True),
        ("0 SEK", "SEK", False),
        ("0 SEK", "USD", True),
        ("0", "SEK", False),
        ("0", "USD", False),
        (-1984.51, "SEK", False),
        ("USD -1984.51", "USD", False),
        ("-1984.51 USD ", "USD", False),
        ("-1984.51 USD USD", "USD", True),
        (Money(1), "USD", False),
        (Money(1, currency="USD"), "USD", False),
        (Money("4711.00 USD", currency="USD"), "USD", False),
        (Money("4711.00"), "USD", False),
        (Money("4711.00 SEK"), "USD", True),
        (None, None, True),
        (False, None, True),
        (True, None, True),
        ("X", None, True),
        (b"1", None, True),
        (b"1.00", None, True),
        (Decimal("1.51"), None, False),
        (1, 1, True),
        (1, True, True),
        (1, ";;;", True),
        ("1 ;;;", None, True),
        (";;; 1", None, True),
        (Money(1, is_cents=True), None, False),
        (Money(1.50, is_cents=True), None, False),
        (Money("1.50", is_cents=True), None, False),
        (Money(Decimal("150"), is_cents=True), None, False),
        (Money(Money("150"), is_cents=True), None, False),
        ("999999999999999999.999999999", None, False),
        ("-999999999999999999.999999999", None, False),
        ("999999999999999999.9999999999", None, True),
        ("-999999999999999999.9999999999", None, True),
        ("1000000000000000000", None, True),
        ("-1000000000000000000", None, True),
    ],
)
def test_input_values(amount: Any, currency: Any, exception_expected: bool) -> None:
    try:
        m = Money(amount, currency=currency)
        if exception_expected:
            assert False, "Exception expected"
        assert m is not None
    except Exception:
        if not exception_expected:
            raise

    assert True
