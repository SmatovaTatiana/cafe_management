from django.urls import path
from . import views

app_name = 'doc_temp'

urlpatterns = [
    path(r'<prev_page>', views.doc_detail, name='doc_detail'),
    path(r'add/<prev_page>', views.doc_add, name='doc_add'),
    path(r'add/<int:product_id><str:prev_page>', views.doc_add, name='doc_add'),
    path(r'remove/<int:product_id><str:prev_page>', views.doc_remove, name='doc_remove'),
]
