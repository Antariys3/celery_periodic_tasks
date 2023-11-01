from django import forms


class ExchangeCalculatorForm(forms.Form):
    amount = forms.DecimalField(label='Сумма', min_value=0, required=True)
    currency_from = forms.ChoiceField(label='Из валюты', choices=[("USD", "USD"), ("EUR", "EUR"), ("UAH", "UAH")])
    currency_to = forms.ChoiceField(label='В валюту', choices=[("USD", "USD"), ("EUR", "EUR"), ("UAH", "UAH")])

    def clean(self):
        cleaned_data = super().clean()
        currency_from = cleaned_data.get('currency_from')
        currency_to = cleaned_data.get('currency_to')

        if currency_from and currency_to and currency_from == currency_to:
            raise forms.ValidationError('Для конвертации валюты должны быть разными')

        forbidden_pairs = [("USD", "EUR"), ("EUR", "USD")]
        if (currency_from, currency_to) in forbidden_pairs or (currency_to, currency_from) in forbidden_pairs:
            raise forms.ValidationError('Конвертация между "USD" и "EUR" не разрешена')
