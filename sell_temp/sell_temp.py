from decimal import Decimal
from django.conf import settings
from cafecrm.models import Drink


class Selltemp(object):

    def __init__(self, request):
        """
        Инициализируем временный документ
        """
        self.session = request.session
        sell = self.session.get(settings.SELLTEMP_SESSION_ID)
        if not sell:
            # save an empty doc in the session
            sell = self.session[settings.SELLTEMP_SESSION_ID] = {}
        self.sell = sell

    def add(self, drink, quantity=1, update_quantity=False):
        """
        Добавить продукт во временный документ или обновить его количество.
        """
        drink_id = str(drink.id)
        if drink_id not in self.sell:
            self.sell[drink_id] = {'quantity': 0}
        if update_quantity:
            self.sell[drink_id]['quantity'] = quantity
        else:
            self.sell[drink_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии doc
        self.session[settings.SELLTEMP_SESSION_ID] = self.sell
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, drink):
        """
        Удаление товара из временного документа.
        """
        drink_id = str(drink.id)
        if drink_id in self.sell:
            del self.sell[drink_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в временном документе и получение продуктов из базы данных.
        """
        drink_ids = self.sell.keys()
        # получение объектов product и добавление их во временный документ
        drinks = Drink.objects.filter(id__in=drink_ids)
        for drink in drinks:
            self.sell[str(drink.id)]['drink'] = drink
        for item in self.sell.values():
            item['quantity'] = item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров во временном документе.
        """
        return sum(item['quantity'] for item in self.sell.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров во временном документе.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.sell.values())

    def clear(self):
        # удаление временного документа из сессии
        del self.session[settings.SELLTEMP_SESSION_ID]
        self.session.modified = True
