import pytest

from decimal import Decimal

from stockholm import Money
import stockholm.currency


def test_conversion_extensions() -> None:
    m1 = Money(50, currency="USD")
    m2 = Money(-50, currency="USD")

    assert m1 == (-m2)
    assert (-m1) == m2

    assert (+m1) == m1

    assert isinstance(abs(m1), Money)
    assert abs(m1) == m1
    assert abs(m2) != m2
    assert abs(m2) == m1

    assert isinstance(int(m1), int)
    assert int(m1) == 50
    assert int(m2) == -50

    assert isinstance(float(m1), float)
    assert float(m1) == 50.00
    assert float(m2) == -50.00


def test_rounding() -> None:
    m1 = Money(50, currency="USD")
    m2 = Money(-50, currency="USD")

    assert round(Money("2.5")) == Money(3)
    assert round(Money("2.5"), 0) == Money(3)
    assert round(Money("2.5"), 1) == Money("2.5")

    m = m1 / 3
    assert isinstance(m, Money)
    assert m != Money("16.666666667", currency="USD")
    assert str(m) == Money("16.666666667", currency="USD")

    m = m2 / 3
    assert isinstance(m, Money)
    assert m != Money("-16.666666667", currency="USD")
    assert str(m) == Money("-16.666666667", currency="USD")

    m = (m1 / 3) * 2
    assert isinstance(m, Money)
    assert m != Money("33.333333333", currency="USD")
    assert str(m) == Money("33.333333333", currency="USD")

    m = (m2 / 3) * 2
    assert isinstance(m, Money)
    assert m != Money("-33.333333333", currency="USD")
    assert str(m) == Money("-33.333333333", currency="USD")

    m = round(m1 / 3, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("16.67", currency="USD")

    m = round(m2 / 3, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("-16.67", currency="USD")

    m = round((m1 / 3) * 2, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("33.33", currency="USD")

    m = round((m2 / 3) * 2, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("-33.33", currency="USD")

    m = round(m1 / 3)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("17", currency="USD")

    m = round(m2 / 3)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("-17", currency="USD")


def test_string_formatting() -> None:
    m = Money("123456.50", currency="GBP")
    assert f"{m}" == "123456.50 GBP"
    assert f"{m:}" == "123456.50 GBP"
    assert f"{m:f}" == "123456.50"
    assert f"{m:.2f}" == "123456.50"
    assert f"{m:.0f}" == "123457"
    assert f"{m:.5f}" == "123456.50000"
    assert f"{m:m}" == "123456.50 GBP"
    assert f"{m:.2m}" == "123456.50 GBP"
    assert f"{m:.0m}" == "123457 GBP"
    assert f"{m:.5m}" == "123456.50000 GBP"
    assert f"{m:-.5m}" == "123456.50000 GBP"
    assert f"{m:+.5m}" == "+123456.50000 GBP"
    assert f"{m: .5m}" == " 123456.50000 GBP"
    assert f"{m:M}" == "GBP 123456.50"
    assert f"{m:.2M}" == "GBP 123456.50"
    assert f"{m:.0M}" == "GBP 123457"
    assert f"{m:.5M}" == "GBP 123456.50000"
    assert f"{m:-.5M}" == "GBP 123456.50000"
    assert f"{m:+.5M}" == "GBP +123456.50000"
    assert f"{m: .5M}" == "GBP  123456.50000"
    assert f"{m:d}" == "123457"
    assert f"{m:+d}" == "+123457"
    assert f"{m: d}" == " 123457"
    assert f"{m:s}" == "123456.50 GBP"
    assert f"{m:c}" == "GBP"

    m = Money(123456, currency="GBP")
    assert f"{m}" == "123456.00 GBP"
    assert f"{m:f}" == "123456.00"
    assert f"{m:.0f}" == "123456"
    assert f"{m:.1f}" == "123456.0"
    assert f"{m:.2f}" == "123456.00"

    m = Money("123457.50", currency="GBP")
    assert f"{m}" == "123457.50 GBP"
    assert f"{m:.2f}" == "123457.50"
    assert f"{m:.0f}" == "123458"
    assert f"{m:.5f}" == "123457.50000"
    assert f"{m:d}" == "123458"

    m = Money(123457, currency="GBP")
    assert f"{m:.2f}" == "123457.00"

    m = Money("-0.01", currency="SEK")
    assert f"{m:.4m}" == "-0.0100 SEK"
    assert f"{m:m}" == "-0.01 SEK"
    assert f"{m:.1m}" == "0.0 SEK"
    assert f"{m:.0m}" == "0 SEK"
    assert f"{m:+m}" == "-0.01 SEK"
    assert f"{m:+.1m}" == "+0.0 SEK"
    assert f"{m:+.0m}" == "+0 SEK"

    m = Money("0.005", currency="SEK")
    assert f"{m:.4m}" == "0.0050 SEK"
    assert f"{m:m}" == "0.005 SEK"
    assert f"{m:.2m}" == "0.01 SEK"
    assert f"{m:.1m}" == "0.0 SEK"
    assert f"{m:.0m}" == "0 SEK"
    assert f"{m:+.4m}" == "+0.0050 SEK"

    m = Money("0.0050", currency="ETH")
    assert f"{m:5.4m}" == "0.0050 ETH"
    assert f"{m:+5.4m}" == "+0.0050 ETH"
    assert f"{m:05.2m}" == "00.01 ETH"
    assert f"{m:+05.2m}" == "+0.01 ETH"
    assert f"{m:05.3m}" == "0.005 ETH"
    assert f"{m:+05.3m}" == "+0.005 ETH"
    assert f"{m:10.4m}" == "    0.0050 ETH"
    assert f"{-m:10.4m}" == "   -0.0050 ETH"
    assert f"{m:+10.4m}" == "   +0.0050 ETH"
    assert f"{m:10.4M}" == "ETH     0.0050"
    assert f"{-m:10.4M}" == "ETH    -0.0050"
    assert f"{m:+10.4M}" == "ETH    +0.0050"
    assert f"{m:10.0m}" == "         0 ETH"
    assert f"{-m:10.0m}" == "         0 ETH"
    assert f"{m:+10.0m}" == "        +0 ETH"
    assert f"{-m:+10.0m}" == "        +0 ETH"
    assert f"{m:010.4m}" == "00000.0050 ETH"
    assert f"{-m:010.4m}" == "-0000.0050 ETH"
    assert f"{m:+010.4m}" == "+0000.0050 ETH"
    assert f"{m: 010.4m}" == " 0000.0050 ETH"
    assert f"{m:+10.4m}" == "   +0.0050 ETH"
    assert f"{-m:010.4M}" == "ETH -0000.0050"
    assert f"{m:+010.4M}" == "ETH +0000.0050"
    assert f"{m:010.0m}" == "0000000000 ETH"
    assert f"{-m:010.0m}" == "0000000000 ETH"
    assert f"{-m:+010.0m}" == "+000000000 ETH"
    assert f"{-m:010.0f}" == "0000000000"

    m = Money("22.12345", currency="ETH")
    assert f"{m:010.5m}" == "0022.12345 ETH"
    assert f"{-m:010.5m}" == "-022.12345 ETH"
    assert f"{-m:10.5m}" == " -22.12345 ETH"
    assert f"{m:010.4m}" == "00022.1235 ETH"
    assert f"{-m:010.4m}" == "-0022.1235 ETH"
    assert f"{-m:10.4m}" == "  -22.1235 ETH"
    assert f"{m:010.3m}" == "000022.123 ETH"
    assert f"{m:+010.3m}" == "+00022.123 ETH"
    assert f"{-m:010.3m}" == "-00022.123 ETH"
    assert f"{-m:10.3m}" == "   -22.123 ETH"
    assert f"{m:+10.3m}" == "   +22.123 ETH"
    assert f"{m:+10.3f}" == "   +22.123"
    assert f"{m:x<15}" == "22.12345 ETHxxx"
    assert f"{m:<15}" == "22.12345 ETH   "
    assert f"{m: <15}" == "22.12345 ETH   "
    assert f"{m: >15}" == "   22.12345 ETH"
    assert f"{m:x<15.3f}" == "22.123xxxxxxxxx"
    assert f"{m:<15}" == "22.12345 ETH   "
    assert f"{-m:=10m}" == "- 22.12345 ETH"
    assert f"{m:=+10m}" == "+ 22.12345 ETH"
    assert f"{-m:x=10m}" == "-x22.12345 ETH"
    assert f"{m:x=+10m}" == "+x22.12345 ETH"

    m = Money("-100030055.05555", currency="SEK")
    assert f"{m:,m}" == "-100,030,055.05555 SEK"
    assert f"{m:,f}" == "-100,030,055.05555"
    assert f"{m:,.2m}" == "-100,030,055.06 SEK"
    assert f"{m:,.2M}" == "SEK -100,030,055.06"
    assert f"{m:,.2f}" == "-100,030,055.06"
    assert f"{m:,.0m}" == "-100,030,055 SEK"
    assert f"{m:,.0f}" == "-100,030,055"

    m = Money("5100030055.05555", currency="SEK")
    assert f"{m:,m}" == "5,100,030,055.05555 SEK"
    assert f"{m:,f}" == "5,100,030,055.05555"

    m = Money("0.5", currency="SEK")
    assert f"{m:,m}" == "0.50 SEK"
    assert f"{m:,f}" == "0.50"
    assert f"{m:,.0m}" == "1 SEK"
    assert f"{m:,.0f}" == "1"

    m = Money("-999.5", currency="SEK")
    assert f"{m:,m}" == "-999.50 SEK"
    assert f"{m:,f}" == "-999.50"
    assert f"{m:,.0m}" == "-1,000 SEK"
    assert f"{m:,.0f}" == "-1,000"

    m = Money(1000)
    assert f"{m}" == "1000.00"
    assert f"{m:}" == "1000.00"
    assert f"{m:s}" == "1000.00"
    assert f"{m:f}" == "1000.00"
    assert f"{m:m}" == "1000.00"
    assert f"{m:.5m}" == "1000.00000"
    assert f"{m:.5f}" == "1000.00000"

    with pytest.raises(ValueError):
        f"{m:x<015.3f}"

    with pytest.raises(ValueError):
        f"{m:<015.3f}"

    with pytest.raises(ValueError):
        f"{m:=15}"

    with pytest.raises(ValueError):
        f"{m:X}"

    with pytest.raises(ValueError):
        f"{m:+s}"

    with pytest.raises(ValueError):
        f"{m:,s}"


def test_string_formatting_sentence() -> None:
    m1 = Money(1352953, "JPY")
    exchange_rate = Decimal("0.08861326")
    m2 = Money(m1 * exchange_rate, "SEK")

    expected = (
        "I have 1,352,953 JPY which equals around 119,889.58 SEK if the exchange rate is 0.08861326 (JPY -> SEK)."
    )
    assert (
        f"I have {m1:,.0m} which equals around {m2:,.2m} if the exchange rate is {exchange_rate} ({m1:c} -> {m2:c})."
        == expected
    )


def test_string_formatting_sentence_currency_types() -> None:
    m1 = Money(1352953, stockholm.currency.JPY)
    exchange_rate = Decimal("0.08861326")
    m2 = round(Money(m1 * exchange_rate, stockholm.currency.SEK), 2)

    expected = (
        "I have 1,352,953 JPY which equals around 119,889.58 SEK if the exchange rate is 0.08861326 (JPY -> SEK)."
    )
    assert (
        f"I have {m1:,m} which equals around {m2:,m} if the exchange rate is {exchange_rate} ({m1:c} -> {m2:c})."
        == expected
    )
