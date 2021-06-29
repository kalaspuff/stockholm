import stockholm.currency
from stockholm import Money, Currency, BaseCurrency, get_currency


assert Money(100, stockholm.currency.EUR) == Money("100 EUR")
assert Money(100, BaseCurrency("SEK")) == Money("100 SEK")
assert Money(100, Currency("USD")) == Money("100 USD")
assert Money(100, Currency.GBP) == Money("100 GBP")
assert Money(100, Currency.DKK) == Money("100 DKK")
assert Money(100, get_currency("JPY")) == Money("100 JPY")
assert Money(100) == Money("100")

assert isinstance(stockholm.currency.EUR, BaseCurrency)
assert isinstance(BaseCurrency("SEK"), BaseCurrency)
assert isinstance(Currency("USD"), BaseCurrency)
assert isinstance(Currency.GBP, BaseCurrency)
assert isinstance(Currency.DKK, BaseCurrency)
assert isinstance(get_currency("JPY"), BaseCurrency)

assert Currency("SEK") == stockholm.currency.SEK == get_currency("SEK") == Currency.SEK == BaseCurrency("SEK")
