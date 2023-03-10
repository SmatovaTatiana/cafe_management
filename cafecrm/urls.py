from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import ProductAddView


app_name='cafecrm'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cafecrm:index'), name='logout'),
    path('add_simple_product', views.add_simple_product, name='add_simple_product'),
    path('stock', views.stock, name='stock'),
    path('menu', views.menu, name='menu'),
    path('products', views.products, name='products'),
    path('products_for_new_drink', views.products_for_new_drink, name='products_for_new_drink'),
    path('drink_create', views.drink_create, name='drink_create'),
    path('document_create', views.document_create, name='document_create'),
    path('drinks', views.drinks, name='drinks'),
    path('selling_document_create', views.selling_document_create, name='selling_document_create'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
 #   path('cafecrm/<slug:slug>', views.drink_detail, name='drink_detail'),



]
