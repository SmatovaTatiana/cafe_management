from django import forms
from django.forms import ModelForm, modelformset_factory, TextInput, Textarea
from .models import Products, Drink, Document, Selling


# login form for index page
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username',
                                                             'class': 'input-field-form'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                                 'class': 'input-field-form'}))


# add new product
class AddProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_type', 'unit']
        PRODUCT_TYPE_CHOICES = [(type, str(type)) for type in Products.PRODUCT_TYPE]
        UNIT_CHOICES = [(unit, str(unit)) for unit in Products.UNITS]
        product_name = forms.TextInput()
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
        fields = ['drink_name', 'menu_type']


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'description']


class SellingDocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Selling
        fields = ['comments']
        widgets = {
            'comments': Textarea(attrs={
                'class': 'comments',
                'placeholder': 'Комментарий к документу',

            }),

        }