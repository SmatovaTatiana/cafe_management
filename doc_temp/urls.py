from django.urls import path
from . import views

app_name = 'doc_temp'

urlpatterns = [
    path(r'', views.doc_detail, name='doc_detail'),
    path(r'add', views.doc_add, name='doc_add'),
    path(r'add/<product_id>', views.doc_add, name='doc_add'),
    path(r'remove/<product_id>', views.doc_remove, name='doc_remove'),
]
