from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.utils.text import slugify
from .models import *
from .forms import AddProductForm, ProductsFormSet
from doc_temp.forms import DoctempAddProductForm


def index(request):
    return render(request, 'cafecrm/index.html', {'title': 'Home'})


def products(request):
    products = Products.objects.all().order_by('product_name')
    doc_product_form = DoctempAddProductForm()
    return render(request,
                  'cafecrm/products.html',
                  {'title': 'Products',
                   'products': products,
                   'doc_product_form': doc_product_form}
                  )


def product_detail(request, slug):
    product = get_object_or_404(Products,
                                slug=slug)
    return render(request,
                  'cafecrm/product_detail.html',
                  {'product': product})


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
