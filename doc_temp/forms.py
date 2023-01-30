from django import forms
from cafecrm.models import Products


class DoctempAddProductForm(forms.Form):
    product_name = forms.ChoiceField(choices=[(item.id, str(item.product_name)) for item in Products.objects.all()], label='Продукт')
    quantity = forms.IntegerField(min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class DoctempUpdateProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
