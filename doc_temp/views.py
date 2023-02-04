from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cafecrm.models import Products
from .doc_temp import Doctemp
from .forms import DoctempAddProductForm, DoctempUpdateProductForm



@require_POST
def doc_add(request, product_id=0, prev_page=''):
    doc = Doctemp(request)
    if prev_page in ['products_for_new_drink', 'drink_create']:
        prev_page = 'new_drink_document'
    elif prev_page in ['products', 'document_create']:
        prev_page = 'stock_document'
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

    return redirect('doc_temp:doc_detail', {'prev_page': prev_page})


def doc_remove(request, product_id=0, prev_page=''):
    doc = Doctemp(request)
    product = get_object_or_404(Products, id=product_id)
    doc.remove(product)
    if prev_page in ['products_for_new_drink', 'drink_create', 'new_drink_document']:
        prev_page = 'new_drink_document'
    elif prev_page in ['products', 'document_create', 'stock_document']:
        prev_page = 'stock_document'

    return redirect('doc_temp:doc_detail', prev_page)


def doc_detail(request, prev_page):
    doc = Doctemp(request)
    referer = str(request.META.get('HTTP_REFERER')).split('/')[-1]
    new_drink = ['products_for_new_drink', 'drink_create', 'new_drink_document']
    new_stock = ['products', 'document_create', 'stock_document']
    key = 0
    if 'stock_document' in prev_page:
        key = 1
    elif 'new_drink_document' in prev_page:
        key = 2
    #prev_page = prev_page.split(':')[-1].strip("'\}").strip(" \'")
    if referer in new_stock or key == 1:
        prev_page = 'stock_document'
    elif referer in new_drink or key == 2:
        prev_page = 'new_drink_document'
    for item in doc:
        item['update_quantity_form'] = DoctempAddProductForm(initial={'quantity': item['quantity'],
                                                                  'update': True})
    context = {
        'doc': doc,
        'prev_page': prev_page,
    }
    return render(request, 'doc_temp/detail.html', context)
