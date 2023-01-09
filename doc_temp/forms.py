from django import forms


class DoctempAddProductForm(forms.Form):
    quantity = forms.IntegerField()
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
