from stockholm import Currency, Money

dict_value = Money(13.50, Currency.SEK).asdict()
assert dict_value["value"] == "13.50 SEK"
assert dict_value["units"] == 13
assert dict_value["nanos"] == 500000000
assert dict_value["currency_code"] == "SEK"

protobuf_value = Money(12984, Currency.JPY).proto()
