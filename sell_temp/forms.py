from django import forms
from cafecrm.models import Drink


class SellAddForm(forms.Form):
    drink_name = forms.ChoiceField(choices=[(item.id, str(item.drink_name)) for item in Drink.objects.all()], label='Товар')
    quantity = forms.IntegerField(min_value=1, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class SellUpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
