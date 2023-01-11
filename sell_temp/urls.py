from django.urls import path
from . import views

app_name = 'sell_temp'

urlpatterns = [
    path(r'', views.sell_detail, name='sell_detail'),
    path(r'<drink_id>/add', views.sell_add, name='sell_add'),
    path(r'<drink_id>/remove', views.sell_remove, name='sell_remove'),
]
