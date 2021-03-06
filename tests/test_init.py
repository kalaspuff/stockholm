import pytest

import stockholm


def test_init() -> None:
    assert stockholm

    assert isinstance(stockholm.__version_info__, tuple)
    assert stockholm.__version_info__
    assert isinstance(stockholm.__version__, str)
    assert len(stockholm.__version__)


def test_money_hashable() -> None:
    m = stockholm.Money(0)
    assert hash(m)


def test_empty_construct() -> None:
    with pytest.raises(stockholm.ConversionError):
        stockholm.Money()
