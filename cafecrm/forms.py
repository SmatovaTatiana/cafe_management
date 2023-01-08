from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import Products, Drink


# for simple form
class AddProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_type', 'unit']
        PRODUCT_TYPE_CHOICES = [(type, str(type)) for type in Products.PRODUCT_TYPE]
        UNIT_CHOICES = [(unit, str(unit)) for unit in Products.UNITS]
        product_name = forms.TextInput
        product_type = forms.TypedChoiceField(choices=PRODUCT_TYPE_CHOICES)
        unit = forms.TypedChoiceField(choices=UNIT_CHOICES)


# for multiply form
ProductsFormSet = modelformset_factory(
    Products,
    fields=('product_name', 'product_type', 'unit'),
    extra=1
    )


class DrinkCreateForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['drink_name']