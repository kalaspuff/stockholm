from decimal import Decimal
import pytest

from stockholm import Money


def test_update_data() -> None:
    m = Money("4711", "SEK")
    assert str(m) == "4711.00 SEK"

    assert m._amount == Decimal(4711)
    assert m._currency == "SEK"

    with pytest.raises(AttributeError):
        m._amount = 10

    with pytest.raises(AttributeError):
        m._currency = "USD"

    assert m._amount == Decimal(4711)
    assert m._currency == "SEK"
