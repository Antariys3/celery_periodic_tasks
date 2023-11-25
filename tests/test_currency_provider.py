from unittest.mock import MagicMock

import responses

from exchange.currency_provider import MonoProvider, SellBuy, PrivatbankProvider, NationalBankProvider, VKurseProvider


def test_mono_currency_provider():
    provider = MonoProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_mono_with_data():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=[
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateBuy": 28.0,
                "rateSell": 28.0,
            }
        ],
    )
    provider = MonoProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=28.0)


@responses.activate
def test_privatbank_provider_with_data():
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        json=[
            {
                "ccy": "USD",
                "base_ccy": "UAH",
                "buy": 30.0,
                "sale": 30.0,
            }
        ],
    )
    provider = PrivatbankProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=30.0, buy=30.0)

@responses.activate
def test_nationalbank_provider_with_data():
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=[
            {
                "cc": "USD",
                "rate": 30.0,
            }
        ],
    )
    provider = NationalBankProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=30.5, buy=30.0)


@responses.activate
def test_vkurse_provider_with_data():
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json={
            "Dollar": {
                "buy": 29.5,
                "sale": 29.0,
            }
        },
    )
    provider = VKurseProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=29.0, buy=29.5)
