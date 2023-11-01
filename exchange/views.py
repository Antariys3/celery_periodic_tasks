from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .forms import ExchangeCalculatorForm
from .models import Rate


def home(request):
    return render(request, "home.html")


def exchange_rates(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "date": rate.date,
                "vendor": rate.provider,
                "currency_a": rate.currency_from,
                "currency_b": rate.currency_to,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }
    return JsonResponse(response_data)


def exchange_calculator(request):
    if request.method == "GET":
        form = ExchangeCalculatorForm()
        return render(request, 'exchange_calculator.html', {'form': form})

    form = ExchangeCalculatorForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        currency_from = form.cleaned_data['currency_from']
        currency_to = form.cleaned_data['currency_to']

        if currency_from == "UAH":
            rate = Rate.objects.filter(currency_from=currency_to, currency_to=currency_from).order_by('-sell').first()
            best_course = rate.sell
            provider = rate.provider
            converted_amount = amount / best_course


        elif currency_from != "UAH":
            rate = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to).order_by('buy').first()
            best_course = rate.buy
            provider = rate.provider
            converted_amount = amount * best_course

        return HttpResponse(
            f"При лучшем курсе {best_course} от {provider}, полученная суммы: {converted_amount:.2f} {currency_to}")

    return render(request, 'exchange_calculator.html', {'form': form})
