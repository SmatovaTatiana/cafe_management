from django import forms
from cafecrm.models import Products

products = Products.objects.all()
product_chois = [(item.id, str(item.product_name)) for item in products]

class DoctempAddProductForm(forms.Form):
    product_name = forms.ChoiceField(choices=product_chois, label='Продукт')
    quantity = forms.IntegerField(min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class DoctempUpdateProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class SelectProductForm(forms.Form):
    productoooo = forms.ChoiceField(choices=product_chois, label='Продукт')

