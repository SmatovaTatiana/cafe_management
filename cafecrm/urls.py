from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ProductAddView

app_name='cafecrm'

urlpatterns = [
    path('', views.index, name='index'),
    path('product_add', ProductAddView.as_view(), name='product_add'),  # for multiply form
    path('products', views.products, name='products'),
    path('create', views.order_create, name='order_create'),
    path('<slug:slug>', views.product_detail, name='product_detail'),

]
