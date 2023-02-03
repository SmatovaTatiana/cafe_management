from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify

from . import forms
from .models import Products, DrinkItem, Drink, DocumentItem, SellingItem
from .forms import AddProductForm, DrinkCreateForm, DocumentCreateForm, SellingDocumentCreateForm
from doc_temp.doc_temp import Doctemp
from doc_temp.forms import DoctempAddProductForm
from sell_temp.forms import SellAddForm
from sell_temp.sell_temp import Selltemp
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse


def index(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request,
                                  'cafecrm/home.html',
                                  )
                else:
                    return HttpResponse('User not active')
            else:
                return HttpResponse('Bad credentials')
    else:
        form = forms.LoginForm()
    return render(request, 'cafecrm/index.html', {'title': 'Home', 'form': form})


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
def add_simple_product(request):
    sent = False
    message = ''
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            try:
                product_name = form.cleaned_data.get('product_name')
                slug = slugify(product_name)
                form.save()
                sent = True
                message = 'Товар успешно добавлен'
            except:
                message = 'Товар с таким названием уже существует'
    else:
        form = AddProductForm()
    context = {
        'form': form,
        'message': message,
        'sent': sent,
    }
    return render(request, 'cafecrm/add_simple_product.html', context)


def drink_create(request):
    doc = Doctemp(request)
    sent = False
    message = ''
    drink_name = ''
    slug = ''
    if request.method == 'POST':
        form = DrinkCreateForm(request.POST)
        if form.is_valid():
            try:
                drink_name = form.cleaned_data.get('drink_name')
                slug = slugify(drink_name)
                drink = form.save()
                sent = True
                message = 'Товар успешно добавлен'
                for item in doc:
                    DrinkItem.objects.create(drink=drink,
                                             product=item['product'],
                                             quantity=item['quantity'])
                # очистка корзины
                doc.clear()
            except:
                message = 'Товар с таким названием уже существует'
    else:
        form = DrinkCreateForm
    context = {
        'form': form,
        'doc': doc,
        'sent': sent,
        'title': 'Create drink',
        'drink_name': drink_name,
        'slug': slug,
        'message': message,
    }
    return render(request, 'cafecrm/drink_create.html', context)


def drinks(request):
    drinks = Drink.objects.all().order_by('drink_name')
    sell_drink_form = SellAddForm()
    context = {
        'title': 'Drinks',
        'drinks': drinks,
        'sell_drink_form': sell_drink_form
    }
    return render(request,
                  'cafecrm/drinks.html', context)


def drink_detail(request, slug):
    drink = get_object_or_404(Drink,
                              slug=slug
                              )
    drink_items = DrinkItem.objects.filter(drink_id=drink.pk)
    context = {
        'drink_items': drink_items,
        'drink': drink
    }
    return render(request,
                  'cafecrm/drink_detail.html', context)


def document_create(request):
    doc = Doctemp(request)
    sent = False
    document = []
    objects = Products.objects.all()
    if request.method == 'POST':
        form = DocumentCreateForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            document = form.save()
            sent = True
            for item in doc:
                DocumentItem.objects.create(document=document,
                                            product=item['product'],
                                            quantity=item['quantity'])
                # update product quantity in stock
                for el in objects:
                    if el.product_name == str(item['product']):
                        if document.document_type == 'Приход':
                            el.stock += item['quantity']
                            el.save()
                        else:
                            if el.stock < item['quantity']:
                                message = 'Недостаточно товара на складе'
                                deficit = item['quantity'] - el.stock
                                context = {
                                    'message': message,
                                    'product': el.product_name,
                                    'quantity': int(item['quantity']),
                                    'stock': el.stock,
                                    'deficit': deficit
                                }
                                return render(request, 'cafecrm/create_document.html', context)
                            else:
                                el.stock -= item['quantity']
                                el.save()
                # clear temp document
            doc.clear()
            document = document

    else:
        form = DocumentCreateForm
    context = {
        'document': document,
        'form': form,
        'doc': doc,
        'sent': sent,
        'title': 'Create document',
    }
    return render(request, 'cafecrm/create_document.html', context)


@login_required()
def selling_document_create(request):
    sell = Selltemp(request)
    sent = False
    selling = []
    if request.method == 'POST':
        form = SellingDocumentCreateForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            selling = form.save()
            sent = True
            for item in sell:
                SellingItem.objects.create(selling=selling,
                                           drink=item['drink'],
                                           quantity=item['quantity'],
                                           )
                prodano = DrinkItem.objects.filter(drink=item['drink'])
                for el in prodano:
                    aga = Products.objects.filter(id=el.product_id)
                    for a in aga:
                        if a.stock < (el.quantity * item['quantity']):
                            message = 'Не хватает количества на складе'
                            deficit = item['quantity'] - a.stock
                            context = {
                                'message': message,
                                'product': el.product,
                                'quantity': int(el.quantity * item['quantity']),
                                'stock': a.stock,
                                'deficit': deficit,
                            }
                            return render(request, 'cafecrm/create_selling_document.html', context)
                        else:
                            a.stock = int(a.stock - (el.quantity * item['quantity']))
                            a.save()
                # clear temp document
            sell.clear()
            selling = selling
    else:
        form = SellingDocumentCreateForm
    context = {
        'selling': selling,
        'form': form,
        'sell': sell,
        'sent': sent,
        'title': 'Create selling document',
    }
    return render(request, 'cafecrm/create_selling_document.html', context)


def stock(request):
    products = Products.objects.filter(product_type='product').order_by('product_name')
    snacks = Products.objects.filter(product_type='snack').order_by('product_name')
    tares = Products.objects.filter(product_type='tare').order_by('product_name')
    return render(request,
                  'cafecrm/stock.html',
                  {'title': 'stock',
                   'products': products,
                   'snacks': snacks,
                   'tares': tares
                   })


def menu(request):
    menu_drinks = Drink.objects.filter(menu_type='drink').order_by('drink_name')
    menu_snack = Drink.objects.filter(menu_type='snack').order_by('drink_name')
    drink_items = DrinkItem.objects.all()
    context = {
        'drink_items': drink_items,
        'menu_drinks': menu_drinks,
        'menu_snack': menu_snack,
    }
    return render(request,
                  'cafecrm/menu.html', context)


def home(request):
    return render(request, 'cafecrm/home.html', {'title': login})


class Logout(LogoutView):
    next_page = reverse_lazy('cafecrm/index.html')
