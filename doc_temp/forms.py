from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class DoctempAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # позволяет пользователю выбрать количество между 1-20. Мы используем поле
    # TypedChoiceField с coerce=int для преобразования ввода в целое число
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
