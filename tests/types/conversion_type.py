from stockholm import Currency, Money, MoneyProtobufMessage, get_currency

# Type hint validation for .asdict()
dict_value = Money(13.50, Currency.SEK).asdict()
assert dict_value["value"] == "13.50 SEK"
assert dict_value["units"] == 13
assert dict_value["nanos"] == 500000000
assert dict_value["currency_code"] == "SEK"

# Type hint validation for .proto()
m1 = Money(12984, Currency.JPY)
protobuf_value: MoneyProtobufMessage = m1.proto()
assert m1.units == protobuf_value.units
assert protobuf_value.units == 12984
assert protobuf_value.nanos == 0
assert protobuf_value.currency_code == "JPY"
m2 = Money(protobuf_value, get_currency(protobuf_value.currency_code))
assert m1 == m2
assert str(m1) == str(m2)
assert m2.units == m1.units
