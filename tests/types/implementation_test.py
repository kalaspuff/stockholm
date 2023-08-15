import stockholm.currency
from stockholm import BaseCurrency, Currency, Money, Number, Rate, get_currency

assert Money(100, stockholm.currency.EUR) == Money("100 EUR")
assert Money(100, BaseCurrency("SEK")) == Money("100 SEK")
assert Money(100, Currency("USD")) == Money("100 USD")
assert Money(100, Currency.GBP) == Money("100 GBP")
assert Money(100, Currency.DKK) == Money("100 DKK")
assert Money(100, get_currency("JPY")) == Money("100 JPY")
assert Money(100) == Money("100")

assert isinstance(BaseCurrency("SEK"), BaseCurrency)
assert isinstance(Currency("USD"), BaseCurrency)
assert isinstance(get_currency("JPY"), BaseCurrency)

assert all(
    [
        isinstance(stockholm.currency.EUR, BaseCurrency),
        isinstance(Currency.GBP, BaseCurrency),
        isinstance(Currency.DKK, BaseCurrency),
    ]
)

assert Currency("SEK") == stockholm.currency.SEK == get_currency("SEK") == Currency.SEK == BaseCurrency("SEK")

assert Money(100, BaseCurrency("SEK")).currency == stockholm.currency.SEK
assert Money(100, BaseCurrency(stockholm.currency.SEK)).currency == stockholm.currency.SEK
assert Money(100, BaseCurrency(Currency.SEK)).currency == stockholm.currency.SEK
assert Money(100, Currency(stockholm.currency.SEK)).currency == stockholm.currency.SEK
assert Money(100, Currency(Currency.SEK)).currency == stockholm.currency.SEK

assert Rate(1).__reduce__() == (Rate, ("1", None))
assert Number(1).__reduce__() == (Number, ("1", None))
assert Rate(Number(100)).__reduce__() == (Rate, ("100", None))
assert Rate(Money(4711)).__reduce__() == (Rate, ("4711", None))
