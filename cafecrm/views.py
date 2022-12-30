from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import *
from .forms import AddProductForm, ProductsFormSet


def index(request):
    return render(request, 'cafecrm/index.html', {'title': 'Home'})


def products(request):
    all_products = Products.objects.all().order_by('product_name')
    return render(request, 'cafecrm/products.html', {'title': 'Products', 'all_products': all_products})


# simple form
def add_product(request):
    sent = False
    error = ''
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            sent = True
            return redirect(reverse_lazy("products"))
        else:
            error = 'Form is not valid'

    form = AddProductForm()
    context = {
        'form': form,
        'error': error,
        'sent': sent
    }
    return render(request, 'cafecrm/add_product.html', context)


# View for adding product multiply form
class ProductAddView(TemplateView):
    template_name = "cafecrm/product_add.html"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        formset = ProductsFormSet(queryset=Products.objects.none())
        return self.render_to_response({'product_formset': formset})

    # Define method to handle POST request
    def post(self, *args, **kwargs):

        formset = ProductsFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("products"))

        return self.render_to_response({'product_formset': formset})
