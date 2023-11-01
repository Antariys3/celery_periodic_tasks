import dataclasses
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


@dataclasses.dataclass
class SellBuy:
    sell: float
    buy: float


class RateNotFound(Exception):
    pass


class ProviderBase(ABC):
    name = None

    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    @abstractmethod
    def get_rate(self) -> SellBuy:
        pass


class MonoProvider(ProviderBase):
    name = "monobank"

    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> SellBuy:
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()

        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency_to_code = self.iso_from_country_code[self.currency_to]

        for currency in response.json():
            if (
                    currency["currencyCodeA"] == currency_from_code
                    and currency["currencyCodeB"] == currency_to_code
            ):
                value = SellBuy(
                    sell=float(currency["rateSell"]), buy=float(currency["rateBuy"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class PrivatbankProvider(ProviderBase):
    name = "privatbank"

    def get_rate(self) -> SellBuy:
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
        response = requests.get(url)
        response.raise_for_status()
        for currency in response.json():
            if (
                    currency["ccy"] == self.currency_from
                    and currency["base_ccy"] == self.currency_to
            ):
                value = SellBuy(
                    buy=float(currency["buy"]), sell=float(currency["sale"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class NationalBankProvider(ProviderBase):
    name = "NationalBank"

    def get_rate(self) -> SellBuy:
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        response = requests.get(url)
        response.raise_for_status()
        for currency in response.json():
            if currency["cc"] == self.currency_from:
                value = SellBuy(
                    # There is no sell parameter in the json file, so I make it by default larger by 0.5
                    buy=float(currency["rate"]), sell=float(currency["rate"] + 0.5)
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


# Ниже не работающий класс, хотя всё распарсено верно. И это класс не работает по тому что значения "buy" и "sell"
# пустые. А пустые они по тому что сайт скрывает от нас эти значения.
class VKurseProvider(ProviderBase):
    name = "VKurse"

    def get_rate(self) -> SellBuy:
        url = "https://vkurse.dp.ua/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        currencies = soup.find_all('div', class_='col-xs-4 section-course')
        for currency in currencies:
            usd_text = currency.find('div', {'class': 'cirlce-value'}).find('p').contents[0].strip()
            if usd_text == self.currency_from:
                value = SellBuy(
                    buy=currency.find('p', {'id': 'dollarBuy', 'class': 'pokupka-value'}).text.strip(),
                    sell=currency.find('p', {'id': 'dollarSale', 'class': 'pokupka-value'}).text.strip()
                )
                return value
            raise RateNotFound(
                f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
            )


# Та же история, что и с предыдущим классом. Этот раз я не делал весь класс, а решил сразу проверить. И снова значения
# с курсом валют пустые.
class MinfinProvider(ProviderBase):
    name = "Minfin"

    def get_rate(self):
        url = "https://minfin.com.ua/ua/currency/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        currencies = soup.find_all('tr', class_='sc-1x32wa2-4 dKDsVV')
        print(currencies[0])


PROVIDERS = [MonoProvider, PrivatbankProvider, NationalBankProvider]

# if __name__ == "__main__":
#     provider = NationalBankProvider("USD", "UAH")
#     print(provider.get_rate())
