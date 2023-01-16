from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Products, DrinkItem, Drink, DocumentItem, SellingItem
from .forms import AddProductForm, DrinkCreateForm, DocumentCreateForm, SellingDocumentCreateForm
from doc_temp.doc_temp import Doctemp
from doc_temp.forms import DoctempAddProductForm
from sell_temp.forms import SellAddForm
from sell_temp.sell_temp import Selltemp


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
def add_simple_product(request):
    sent = False
    error = ''
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data.get('product_name')
            slug = slugify(product_name)
            form.save()
            sent = True
            return redirect(reverse_lazy("cafecrm:products"))
        else:
            error = 'Form is not valid'

    form = AddProductForm()
    context = {
        'form': form,
        'error': error,
        'sent': sent,

    }
    return render(request, 'cafecrm/add_simple_product.html', context)


'''# View for adding product multiply form
class ProductAddView(TemplateView):
    template_name = "cafecrm/product_add.html"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        formset = ProductsFormSet(queryset=Products.objects.none())
        return self.render_to_response({'product_formset': formset})

    # Define method to handle POST request
    def post(self, *args, **kwargs):
        formset = ProductsFormSet(data=self.request.POST)
        if formset.is_valid():
            product_name = formset.cleaned_data.get('product_name')
            slug = slugify(product_name)
            formset.save()
            return redirect(reverse_lazy('cafecrm:products'))

        return self.render_to_response({'product_formset': formset})'''


def drink_create(request):
    doc = Doctemp(request)
    sent = False
    drink_name = ''
    slug = ''
    if request.method == 'POST':
        form = DrinkCreateForm(request.POST)
        if form.is_valid():
            drink_name = form.cleaned_data.get('drink_name')
            slug = slugify(drink_name)
            drink = form.save()
            sent = True
            for item in doc:
                DrinkItem.objects.create(drink=drink,
                                         product=item['product'],
                                         quantity=item['quantity'])
            # очистка корзины
            doc.clear()
    else:
        form = DrinkCreateForm
    context = {
        'form': form,
        'doc': doc,
        'sent': sent,
        'title': 'Create drink',
        'drink_name': drink_name,
        'slug': slug
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
 #   message = ''
    if request.method == 'POST':
        form = DocumentCreateForm(request.POST)
        if form.is_valid():
            document = form.save()
            sent = True
            for item in doc:
                DocumentItem.objects.create(document=document,
                                         product=item['product'],
                                         quantity=item['quantity'])
                # update product quantity in stock
                for el in objects:
                    if el.product_name == str(item['product']):
                        if document.document_type == 'Receipt':
                            el.stock += item['quantity']
                            el.save()
                        else:
                            if el.stock < item['quantity']:
                                message = 'Не хватает количества на складе'
                                context = {
                                    'message': message,
                                    'product': el.product_name,
                                    'quantity': int(item['quantity']),
                                    'stock': el.stock
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


def selling_document_create(request):
    sell = Selltemp(request)
    sent = False
    selling = []
    if request.method == 'POST':
        form = SellingDocumentCreateForm(request.POST)
        if form.is_valid():
            selling = form.save()
            sent = True
            for item in sell:
                SellingItem.objects.create(selling=selling,
                                         drink=item['drink'],
                                         quantity=item['quantity'])

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
        'title': 'Create selling document'
    }
    return render(request, 'cafecrm/create_selling_document.html', context)


def stock(request):
    products = Products.objects.all().order_by('product_name')
    return render(request,
                  'cafecrm/stock.html',
                  {'title': 'stock',
                   'products': products
                   })


def menu(request):
    menu = Drink.objects.all().order_by('drink_name')
    drink_items = DrinkItem.objects.all()
    context = {
        'drink_items': drink_items,
        'menu': menu
    }
    return render(request,
                  'cafecrm/menu.html', context)