from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cafecrm.models import Drink
from .sell_temp import Selltemp
from .forms import SellAddForm


@require_POST
def sell_add(request, drink_id):
    sell = Selltemp(request)
    drink = get_object_or_404(Drink, id=drink_id)
    form = SellAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        sell.add(drink=drink,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('sell_temp:sell_detail')


def sell_remove(request, drink_id):
    sell = Selltemp(request)
    drink = get_object_or_404(Drink, id=drink_id)
    sell.remove(drink)
    return redirect('sell_temp:sell_detail')


def sell_detail(request):
    sell = Selltemp(request)
    for item in sell:
        item['update_quantity_form'] = SellAddForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'sell_temp/sell_detail.html', {'sell': sell})
