from decimal import Decimal
import pytest

from stockholm import Money


def test_update_data() -> None:
    m = Money("4711", "SEK")
    assert str(m) == "4711.00 SEK"

    assert m.amount == Decimal(4711)
    assert m.currency == "SEK"
    assert m.metadata == {"is_cents": None}

    with pytest.raises(AttributeError):
        m._amount = Decimal(10)

    with pytest.raises(AttributeError):
        m._currency = "USD"

    with pytest.raises(AttributeError):
        m._metadata = {}

    assert m.amount == Decimal(4711)
    assert m.currency == "SEK"

    with pytest.raises(AttributeError):
        del m._amount
