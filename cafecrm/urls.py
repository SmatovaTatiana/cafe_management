from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ProductAddView

# app_name='cafecrm'

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    # You can't have these two URL patterns. Django will always match the top one.
    # The typical solution is to add a prefix to one (or both) of the regexes. I added to product_add 'cafecrm'
    path('cafecrm/product_add', ProductAddView.as_view(), name='product_add'),  # for multiply form
    # path('add_product', views.add_product, name='add_product'),  # for simple form

]
