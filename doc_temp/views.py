from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cafecrm.models import Products
from .doc_temp import Doctemp
from .forms import DoctempAddProductForm, DoctempUpdateProductForm



@require_POST
def doc_add(request, product_id=0):
    doc = Doctemp(request)
    if product_id:
        product = get_object_or_404(Products, id=product_id)
        form = DoctempUpdateProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            doc.add(product=product,
                    quantity=cd['quantity'],
                    update_quantity=cd['update'])
    else:
            form = DoctempAddProductForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                product_id = form.cleaned_data.get('product_name')
                product = Products.objects.get(id=product_id)
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
    for item in doc:
        item['update_quantity_form'] = DoctempAddProductForm(initial={'quantity': item['quantity'],
                                                                  'update': True})
    return render(request, 'doc_temp/detail.html', {'doc': doc})
