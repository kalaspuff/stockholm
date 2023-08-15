import pickle
from copy import copy, deepcopy

from stockholm.currency import Currency
from stockholm.money import Money
from stockholm.rate import Number, Rate


def test_expected() -> None:
    assert str(Money("1012312112312.1412312321", "JPY")._amount) == "1012312112312.1412312321"
    assert Money("1012312112312.1412312321", "JPY").nanos == 141231232
    assert str(Money("1012312112312.1412312321", "JPY")) == "1012312112312.141231232 JPY"
    assert str(Money("1012312112312.1412312321", Currency.JPY)) == "1012312112312.141231232 JPY"
    assert str(Money(0)._amount) == "0"
    assert str(Money(-0)._amount) == "0"
    assert str(Money("-0")._amount) == "0"
    assert str(Money(0.01)._amount) == "0.01"
    assert str(Money(-0.999)._amount) == "-0.999"
    assert str(Money(-0.999999999)) == "-0.999999999"
    assert str(Money(-0.999999999)._amount) == "-0.999999999"
    assert str(Money(-0.9999999999)) == "-1.00"
    assert str(Money(-0.9999999999)._amount) == "-0.9999999999"
    assert str(Money(1000.5)._amount) == "1000.5"


def test_deepcopy_money() -> None:
    m = Money(4711.1338, "SEK")
    m2 = deepcopy(m)

    assert m == m2
    assert m is m2
    assert m.currency == m2.currency
    assert m.currency is m2.currency

    m = Money(-1, Currency.JPY)
    m2 = deepcopy(m)

    assert m == m2
    assert m is m2
    assert m.currency == m2.currency
    assert m.currency is m2.currency


def test_deepcopy_numerics() -> None:
    n = Number(1338.50)
    n2 = deepcopy(n)

    assert n == n2
    assert n is n2

    r = Rate(0.01)
    r2 = deepcopy(r)

    assert r == r2
    assert r is r2


def test_copy_money() -> None:
    m = Money(100.499999, "USD")
    m2 = copy(m)

    assert m == m2
    assert m is m2
    assert m.currency == m2.currency
    assert m.currency is m2.currency

    m = Money(-0, Currency.EUR)
    m2 = copy(m)

    assert m == m2
    assert m is m2
    assert m.currency == m2.currency
    assert m.currency is m2.currency


def test_copy_numerics() -> None:
    n = Number(1338.50)
    n2 = copy(n)

    assert n == n2
    assert n is n2

    r = Rate(0.01)
    r2 = copy(r)

    assert r == r2
    assert r is r2


def test_copy_money_with_currency_object() -> None:
    m = Money(0, Currency.GBP)
    m2 = deepcopy(m)

    assert m == m2
    assert m is m2
    assert m.currency is m2.currency


def test_copy_currency() -> None:
    assert Currency.SEK is Currency.SEK
    assert copy(Currency.SEK) is Currency.SEK
    assert id(copy(Currency.SEK)) == id(Currency.SEK)
    assert id(copy(Currency.JPY)) != id(Currency.SEK)
    assert deepcopy(Currency.SEK) is Currency.SEK
    assert id(deepcopy(Currency.SEK)) == id(Currency.SEK)
    assert id(deepcopy(Currency.JPY)) != id(Currency.SEK)


def test_reduce() -> None:
    assert Money(100).__reduce__() == (Money, ("100", None))
    assert Money(0.01).__reduce__() == (Money, ("0.01", None))
    assert Money("-100.50 SEK").__reduce__() == (Money, ("-100.50", "SEK"))
    assert Money(31338559, Currency.USD).__reduce__() == (Money, ("31338559", Currency.USD))
    assert Money("1012312112312.1412312321", "JPY").__reduce__() == (Money, ("1012312112312.1412312321", "JPY"))
    assert Money("-1012312112312.1412312321 EUR").__reduce__() == (Money, ("-1012312112312.1412312321", "EUR"))


def test_reduce_numerics() -> None:
    assert Number(100).__reduce__() == (Number, ("100", None))
    assert Number(0.01).__reduce__() == (Number, ("0.01", None))
    assert Number("-100.50").__reduce__() == (Number, ("-100.50", None))
    assert Number("1012312112312.1412312321").__reduce__() == (Number, ("1012312112312.1412312321", None))
    assert Number("-1012312112312.1412312321").__reduce__() == (Number, ("-1012312112312.1412312321", None))

    assert Rate(1).__reduce__() == (Rate, ("1", None))
    assert Rate(31338559.1).__reduce__() == (Rate, ("31338559.1", None))


def test_pickle() -> None:
    m = Money(100, "EUR")
    data = pickle.dumps(m)
    m2 = pickle.loads(data)

    assert m == m2
    assert m is not m2
    assert m.currency == m2.currency

    m = Money("1012312112312.1412312321", Currency.CNY)
    data = pickle.dumps(m)
    m2 = pickle.loads(data)

    assert m == m2
    assert m is not m2
    assert m.currency == m2.currency
    assert m.currency is m2.currency

    n = Number("1012312112312.1412312321")
    data = pickle.dumps(n)
    n2 = pickle.loads(data)
    assert n2.__reduce__() == (Number, ("1012312112312.1412312321", None))
    assert copy(n2).__reduce__() == (Number, ("1012312112312.1412312321", None))
    assert deepcopy(n2).__reduce__() == (Number, ("1012312112312.1412312321", None))


def test_copy_list() -> None:
    lst = [Money(100, "EUR"), "abc", "def", Money(200, "USD"), Number(0.01)]
    lst2 = copy(lst)
    lst3 = deepcopy(lst)

    assert lst == lst2
    assert lst == lst3
    assert [id(x) for x in lst] == [id(x) for x in lst2]
    assert [id(x) for x in lst] == [id(x) for x in lst3]
    assert lst3[0] == Money("100 EUR")


def test_copy_tuple() -> None:
    t = [Money("4711.50 EUR"), 1338, 0, Number(0.01), Rate("-0.5")]
    t2 = copy(t)
    t3 = deepcopy(t)

    assert t == t2
    assert t == t3
    assert [id(x) for x in t] == [id(x) for x in t2]
    assert [id(x) for x in t] == [id(x) for x in t3]
    assert t3[0] == Money("4711.50", "EUR")
    assert t3[3] == 0.01
    assert t3[3] == Number(0.01)


def test_copy_dict() -> None:
    d = {"m": Money("-5.5", Currency.SEK), "n": Number(0.01), "r": Rate(25.3)}
    d2 = copy(d)
    d3 = deepcopy(d)

    assert d == d2
    assert d == d3
    assert [id(v) for k, v in d.items()] == [id(v) for k, v in d2.items()]
    assert [id(v) for k, v in d.items()] == [id(v) for k, v in d3.items()]
    assert d3["m"] == -5.5
    assert d3["m"].currency == "SEK"
    assert d3["m"].currency is Currency.SEK
    assert str(d3["m"]) == "-5.50 SEK"
    assert d2["r"].__reduce__() == (Rate, ("25.3", None))
