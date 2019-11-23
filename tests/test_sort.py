import pytest

from stockholm import Money, CurrencyMismatchError


def test_sort_numbers() -> None:
    lst = [
        Money("1"),
        Money("-1"),
        Money("0"),
        Money("4711"),
        77.95,
        Money("4711.55"),
        Money("4711", currency="SEK"),
        Money("4711"),
        Money("0 SEK"),
        3.14,
        Money("1e-2", currency="SEK", is_cents=True),
        Money("-0.5 SEK"),
        -55,
        Money(0.4),
    ]

    expected = [
        -55,
        Money("-1"),
        Money("-0.5 SEK"),
        Money("0"),
        Money("0 SEK"),
        Money("1e-2", currency="SEK", is_cents=True),
        Money(0.4),
        Money("1"),
        3.14,
        77.95,
        Money("4711"),
        Money("4711", currency="SEK"),
        Money("4711"),
        Money("4711.55"),
    ]

    assert lst != expected

    lst.sort()

    assert lst == expected


def test_sort_with_strings() -> None:
    lst = [
        Money("1"),
        Money("-1"),
        Money("0"),
        Money("4711"),
        77.95,
        Money("4711.55"),
        Money("4711", currency="SEK"),
        Money("4711"),
        Money("0 SEK"),
        "1338",
        3.14,
        Money("1e-2", currency="SEK", is_cents=True),
        "0.3351 SEK",
        Money("-0.5 SEK"),
        -55,
        Money(0.4),
    ]

    expected = [
        -55,
        Money("-1"),
        Money("-0.5 SEK"),
        Money("0"),
        Money("0 SEK"),
        Money("1e-2", currency="SEK", is_cents=True),
        "0.3351 SEK",
        Money(0.4),
        Money("1"),
        3.14,
        77.95,
        "1338",
        Money("4711"),
        Money("4711", currency="SEK"),
        Money("4711"),
        Money("4711.55"),
    ]

    assert lst != expected

    with pytest.raises(TypeError):
        lst.sort()

    assert lst != expected

    lst.sort(key=lambda x: Money(x))

    assert lst == expected


def test_sorted_with_strings() -> None:
    lst = [
        Money("1"),
        Money("-1"),
        Money("0"),
        Money("4711"),
        77.95,
        Money("4711.55"),
        Money("4711", currency="SEK"),
        Money("4711"),
        Money("0 SEK"),
        "1338",
        3.14,
        Money("1e-2", currency="SEK", is_cents=True),
        "0.3351 SEK",
        Money("-0.5 SEK"),
        -55,
        Money(0.4),
    ]

    expected = [
        -55,
        Money("-1"),
        Money("-0.5 SEK"),
        Money("0"),
        Money("0 SEK"),
        Money("1e-2", currency="SEK", is_cents=True),
        "0.3351 SEK",
        Money(0.4),
        Money("1"),
        3.14,
        77.95,
        "1338",
        Money("4711"),
        Money("4711", currency="SEK"),
        Money("4711"),
        Money("4711.55"),
    ]

    assert sorted(lst, key=lambda x: Money(x)) == expected
    assert Money.sort(lst) == expected
    assert Money.sort(lst, reverse=True) == list(reversed(expected))


def test_sort_with_differing_currencies() -> None:
    lst = [
        Money("1", currency="SEK"),
        Money("-1", currency="USD"),
    ]

    with pytest.raises(CurrencyMismatchError):
        lst.sort()

    with pytest.raises(CurrencyMismatchError):
        sorted(lst)

    with pytest.raises(CurrencyMismatchError):
        sorted(lst, key=Money)

    with pytest.raises(CurrencyMismatchError):
        Money.sort(lst)
