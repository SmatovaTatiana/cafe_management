from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cafecrm.models import Products
from .doc_temp import Doctemp
from .forms import DoctempAddProductForm


@require_POST
def doc_add(request, product_id):
    doc = Doctemp(request)
    product = get_object_or_404(Products, id=product_id)
    form = DoctempAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        doc.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('doc_temp:doc_detail')


def doc_remove(request, product_id):
    doc = Doctemp(request)
    product = get_object_or_404(Products, id=product_id)
    doc.remove(product)
    return redirect('doc_temp:doc_detail')


def doc_detail(request):
    doc = Doctemp(request)
    return render(request, 'doc_temp/detail.html', {'doc': doc})