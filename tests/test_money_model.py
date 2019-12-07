from stockholm.money import MoneyModel


def test_money_model_from_dict():
    d = {"value": "13384711 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}
    assert str(MoneyModel.from_dict(d)) == "13384711.00 JPY"
