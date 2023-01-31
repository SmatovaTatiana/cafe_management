from django import forms
from cafecrm.models import Products, Drink


class DoctempAddProductForm(forms.Form):
    product_name = forms.ChoiceField(choices=[(item.id, str(item.product_name)) for item in Products.objects.all()], label='Товар')
    quantity = forms.IntegerField(min_value=1, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)



class DoctempUpdateProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class SellAddForm(forms.Form):
    drink_name = forms.ChoiceField(choices=[(item.id, str(item.drink_name)) for item in Drink.objects.all()], label='Товар')
    quantity = forms.IntegerField(min_value=1, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class SellUpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)