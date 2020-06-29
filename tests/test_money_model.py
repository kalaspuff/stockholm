from stockholm import MoneyProtoMessage
from stockholm.money import MoneyModel


def test_money_model_from_dict():
    input_dict = {"value": "13384711 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}
    assert str(MoneyModel.from_dict(input_dict)) == "13384711.00 JPY"


def test_money_model_from_json():
    input_value = '{"value": "13384711 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}'
    assert str(MoneyModel.from_json(input_value)) == "13384711.00 JPY"
    assert (
        MoneyModel.from_json(input_value).as_json()
        == '{"value": "13384711.00 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}'
    )


def test_money_model_from_protobuf_bytes():
    input_proto_bytes = b"\n\x03JPY\x10\x87\xf8\xb0\x06"
    assert str(MoneyModel.from_protobuf(input_proto_bytes)) == "13384711.00 JPY"

    assert (
        MoneyModel.from_protobuf(input_proto_bytes).as_protobuf().SerializeToString()
        == b"\n\x03JPY\x10\x87\xf8\xb0\x06"
    )


def test_money_model_from_protobuf():
    input_proto_message = MoneyProtoMessage.FromString(b"\n\x03JPY\x10\x87\xf8\xb0\x06")
    assert str(MoneyModel.from_protobuf(input_proto_message)) == "13384711.00 JPY"
