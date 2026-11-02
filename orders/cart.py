import uuid
from decimal import Decimal

from django.core.files.storage import default_storage

from merch.models import Product, Variant

CART_KEY = 'cart'
MAX_QTY = 20


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.data = dict(self.session.get(CART_KEY, {}))
        self._lines = None

    def _save(self):
        self.session[CART_KEY] = self.data
        self._lines = None

    @property
    def count(self):
        """Количество штук (без обращения к БД, для шапки сайта)."""
        return sum(item['qty'] for item in self.data.values())

    def add(self, product, variant, text='', image_path='', quantity=1):
        if not image_path:
            for item in self.data.values():
                if (
                    item['product_id'] == product.pk
                    and item['variant'] == variant
                    and item['text'] == text
                    and not item['image']
                ):
                    item['qty'] = min(item['qty'] + quantity, MAX_QTY)
                    self._save()
                    return
        self.data[uuid.uuid4().hex] = {
            'product_id': product.pk,
            'variant': variant,
            'text': text,
            'image': image_path,
            'qty': min(quantity, MAX_QTY),
        }
        self._save()

    def set_qty(self, item_id, qty):
        if item_id not in self.data:
            return
        if qty < 1:
            self.remove(item_id)
            return
        self.data[item_id]['qty'] = min(qty, MAX_QTY)
        self._save()

    def remove(self, item_id):
        # Файл не удаляем: на него может ссылаться уже созданный заказ.
        if self.data.pop(item_id, None) is not None:
            self._save()

    def clear(self):
        self.data = {}
        self._save()

    def restore_from_order(self, order):
        """Возвращает позиции заказа в корзину (при отмене оплаты)."""
        for item in order.items.all():
            product = item.product
            if product is None or not product.is_active:
                continue  # товар удалён или снят с продажи
            self.add(
                product,
                variant=item.variant,
                text=item.text,
                image_path=item.custom_image.name if item.custom_image else '',
                quantity=item.quantity,
            )

    def lines(self):
        """Позиции корзины с актуальными ценами из БД. Товары, снятые с продажи, пропускаются."""
        if self._lines is None:
            products = Product.objects.in_bulk(
                [i['product_id'] for i in self.data.values()]
            )
            lines = []
            for item_id, item in self.data.items():
                product = products.get(item['product_id'])
                if not product or not product.is_active:
                    continue
                unit = product.price_for(item['variant'])
                if item['image']:
                    image_url = default_storage.url(item['image'])
                else:
                    image_url = product.image.url if product.image else ''
                lines.append(
                    {
                        'id': item_id,
                        'product': product,
                        'variant': item['variant'],
                        'variant_label': Variant(item['variant']).label,
                        'text': item['text'],
                        'image': item['image'],
                        'image_url': image_url,
                        'qty': item['qty'],
                        'unit_price': unit,
                        'total': unit * item['qty'],
                    }
                )
            self._lines = lines
        return self._lines

    @property
    def total_price(self):
        return sum((line['total'] for line in self.lines()), Decimal(0))
