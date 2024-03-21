class MoneyExceptionError(Exception):
    pass


# deprecated: use `MoneyExceptionError` instead of `MoneyException`
class MoneyException(MoneyExceptionError):  # noqa: N818
    pass


class CurrencyMismatchError(MoneyException, ValueError):
    pass


class ConversionError(MoneyException, ValueError):
    pass


class InvalidOperandError(MoneyException, TypeError):
    pass
