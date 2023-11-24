from decimal import Decimal
from unittest.mock import patch, Mock

import pytest

from exchange.models import Rate


# @pytest.fixture(scope="session")
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command("loaddata", "rates.json")


# @pytest.fixture
# def mock_rate_filter():
#     with open("exchange/fixtures/rates.json", "r") as file:
#         mock_data = json.load(file)
#     return patch(
#         "exchange.views.Rate.objects.filter",
#         return_value=Mock(
#             order_by=Mock(return_value=Mock(first=Mock(side_effect=mock_data)))
#         ),
#     )
rates_list = [
            {
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal(39.7994),
                "buy": Decimal(38.32),
                "provider": "monobank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.rate",
                "pk": 14,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 37.4406,
                "buy": 36.24,
                "provider": "monobank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 15,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": 40.25,
                "buy": 39.25,
                "provider": "privatbank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 16,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 37.6,
                "buy": 37,
                "provider": "privatbank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 17,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": 38.7311,
                "buy": 38.2311,
                "provider": "NationalBank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 18,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 36.7655,
                "buy": 36.2655,
                "provider": "NationalBank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 19,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": 39.8502,
                "buy": 38.45,
                "provider": "monobank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 20,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 37.4406,
                "buy": 36.26,
                "provider": "monobank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 21,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": 40.25,
                "buy": 39.25,
                "provider": "privatbank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 22,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 37.6,
                "buy": 37,
                "provider": "privatbank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 23,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": 39.1703,
                "buy": 38.6703,
                "provider": "NationalBank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 24,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 36.7659,
                "buy": 36.2659,
                "provider": "NationalBank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 25,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": 40.2,
                "buy": 40.05,
                "provider": "VKurse",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 26,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": 37.85,
                "buy": 37.65,
                "provider": "VKurse",
                "date": "2023-11-02",
            },
        ]



def mock_rates_generator():
    """
    List of Mocks for each rate
    """

    return [
        Mock(spec=Rate, **rate_data)
        for rate_data in rates_list
    ]


@pytest.fixture
def mock_rate_filter():
    mock_rates = mock_rates_generator()

    return patch(
        "exchange.views.Rate.objects.filter",
        return_value=Mock(
            order_by=Mock(
                return_value=Mock(
                    first=Mock(
                        side_effect=mock_rates)))
        ),
    )
