from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ProductAddView

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    #path('add_product', views.add_product, name='add_product'),  # for simple form
    path('product_add', ProductAddView.as_view(), name='product_add'),  # for multiply form
]
