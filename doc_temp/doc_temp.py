from decimal import Decimal
from django.conf import settings
from cafecrm.models import Products


class Doctemp(object):

    def __init__(self, request):
        """
        Инициализируем временный документ
        """
        self.session = request.session
        doc = self.session.get(settings.DOCTEMP_SESSION_ID)
        if not doc:
            # save an empty doc in the session
            doc = self.session[settings.DOCTEMP_SESSION_ID] = {}
        self.doc = doc

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт во временный документ или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.doc:
            self.doc[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.doc[product_id]['quantity'] = quantity
        else:
            self.doc[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии doc
        self.session[settings.DOCTEMP_SESSION_ID] = self.doc
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из временного документа.
        """
        product_id = str(product.id)
        if product_id in self.doc:
            del self.doc[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в временном документе и получение продуктов из базы данных.
        """
        product_ids = self.doc.keys()
        # получение объектов product и добавление их во временный документ
        products = Products.objects.filter(id__in=product_ids)
        for product in products:
            self.doc[str(product.id)]['product'] = product

        for item in self.doc.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров во временном документе.
        """
        return sum(item['quantity'] for item in self.doc.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров во временном документе.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.doc.values())

    def clear(self):
        # удаление временного документа из сессии
        del self.session[settings.DOCTEMP_SESSION_ID]
        self.session.modified = True
