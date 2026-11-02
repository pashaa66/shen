from decimal import Decimal

from django.conf import settings


def calculate_shipping(items_total, address=''):
    """MVP: фиксированная ставка. Сюда позже подключается расчёт через API СДЭК / Почты России."""
    return Decimal(str(settings.SHIPPING_PRICE))
