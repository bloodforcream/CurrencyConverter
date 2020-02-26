from django import forms


class ConvertCurrencyForm(forms.Form):
    convert_from = forms.ChoiceField(choices=[])
    convert_into = forms.ChoiceField(choices=[])
    amount = forms.FloatField()

    def set_currency_choices(self, currency):
        self.fields['convert_from'].choices = [(cur, cur) for cur in currency]
        self.fields['convert_into'].choices = [(cur, cur) for cur in currency]
