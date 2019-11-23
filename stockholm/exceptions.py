class MoneyException(Exception):
    pass


class CurrencyMismatchError(MoneyException, ValueError):
    pass


class ConversionError(MoneyException, ValueError):
    pass


class InvalidOperandError(MoneyException, TypeError):
    pass
