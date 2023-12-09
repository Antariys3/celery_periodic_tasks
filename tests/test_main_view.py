import pytest
from django.test import Client
from django.test import RequestFactory
from django.urls import reverse

from exchange.forms import ExchangeCalculatorForm
from exchange.models import Rate
from exchange.views import exchange_calculator


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_exchange_calculator_view_get(client):
    response = client.get(reverse("exchange_calculator"))
    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], ExchangeCalculatorForm)
    assert b"form" in response.content


@pytest.mark.django_db
def test_exchange_calculator_view_post_valid_data(client):
    Rate.objects.create(
        currency_from="USD",
        currency_to="UAH",
        sell=37.44,
        buy=38.32,
        provider="monobank",
    )

    data = {
        "amount": 100,
        "currency_from": "UAH",
        "currency_to": "USD",
    }

    response = client.post(reverse("exchange_calculator"), data)
    assert response.status_code == 200
    assert "При лучшем курсе".encode("utf-8") in response.content


TESTDATA = [
    (
        {"amount": 1000, "currency_from": "UAH", "currency_to": "EUR"},
        "При лучшем курсе 40.25 от privatbank, полученная сумма: 24.84 EUR",
    ),
    (
        {"amount": 100, "currency_from": "EUR", "currency_to": "UAH"},
        "При лучшем курсе 38.23 от NationalBank, полученная сумма: 3823.11 UAH",
    ),
    (
        {"amount": 1000, "currency_from": "UAH", "currency_to": "USD"},
        "При лучшем курсе 37.85 от VKurse, полученная сумма: 26.42 USD",
    ),
    (
        {"amount": 100, "currency_from": "USD", "currency_to": "UAH"},
        "При лучшем курсе 36.24 от monobank, полученная сумма: 3624.00 UAH",
    ),
]


@pytest.mark.parametrize("request_data, expected_result", TESTDATA)
@pytest.mark.django_db
def test_exchange_calculator(request_data, expected_result):
    request = RequestFactory().post("/", request_data)
    response = exchange_calculator(request)

    response_body = response.content.decode("utf-8")
    assert response_body == expected_result
