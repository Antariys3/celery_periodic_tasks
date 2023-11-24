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


@pytest.mark.django_db
def test_exchange_calculator_with_mock_db(mock_rate_filter):
    with mock_rate_filter:
        request_data = {"amount": 100, "currency_from": "UAH", "currency_to": "USD"}
        request = RequestFactory().post("/", request_data)
        response = exchange_calculator(request)

    response_body = response.content.decode("utf-8")
    expected_result = "При лучшем курсе 39.80 от monobank, полученная суммы: 2.51 USD"
    assert response_body == expected_result
