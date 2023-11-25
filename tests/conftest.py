from decimal import Decimal
from unittest.mock import patch, Mock

import pytest

from exchange.models import Rate


@pytest.fixture
def mock_rate_filter():
    mock_rates = [
        Mock(spec=Rate, **rate_data)
        for rate_data in [
            {
                "model": "exchange.rate",
                "pk": 12,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("39.7994"),
                "buy": Decimal("38.32"),
                "provider": "monobank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.rate",
                "pk": 14,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("37.4406"),
                "buy": Decimal("36.24"),
                "provider": "monobank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 15,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("40.25"),
                "buy": Decimal("39.25"),
                "provider": "privatbank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 16,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("37.6"),
                "buy": Decimal("37"),
                "provider": "privatbank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 17,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("38.7311"),
                "buy": Decimal("38.2311"),
                "provider": "NationalBank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 18,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("36.7655"),
                "buy": Decimal("36.2655"),
                "provider": "NationalBank",
                "date": "2023-11-01",
            },
            {
                "model": "exchange.Rate",
                "pk": 19,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("39.8502"),
                "buy": Decimal("38.45"),
                "provider": "monobank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 20,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("37.4406"),
                "buy": Decimal("36.26"),
                "provider": "monobank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 21,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("40.25"),
                "buy": Decimal("39.25"),
                "provider": "privatbank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 22,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("37.6"),
                "buy": Decimal("37"),
                "provider": "privatbank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 23,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("39.1703"),
                "buy": Decimal("38.6703"),
                "provider": "NationalBank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 24,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("36.7659"),
                "buy": Decimal("36.2659"),
                "provider": "NationalBank",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 25,
                "currency_from": "EUR",
                "currency_to": "UAH",
                "sell": Decimal("40.2"),
                "buy": Decimal("40.05"),
                "provider": "VKurse",
                "date": "2023-11-02",
            },
            {
                "model": "exchange.Rate",
                "pk": 26,
                "currency_from": "USD",
                "currency_to": "UAH",
                "sell": Decimal("37.85"),
                "buy": Decimal("37.65"),
                "provider": "VKurse",
                "date": "2023-11-02",
            },
        ]
    ]

    return patch(
        "exchange.views.Rate.objects.filter",
        return_value=Mock(
            order_by=Mock(return_value=Mock(first=Mock(side_effect=mock_rates)))
        ),
    )
