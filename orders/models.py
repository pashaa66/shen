import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from merch.models import Product, Variant


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Ожидает оплаты'
        PAID = 'paid', 'Оплачен'
        CANCELLED = 'cancelled', 'Отменён'

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders',
    )

    full_name = models.CharField('ФИО', max_length=200)
    email = models.EmailField('Почта')
    bank = models.CharField('Банк', max_length=100)
    address = models.TextField('Адрес доставки')
    phone = models.CharField(
        'Телефон',
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                r'^[\d\s+()\-]{6,20}$', 'Введите корректный номер телефона.'
            )
        ],
    )
    nickname = models.CharField(
        'Ник (Telegram / VK)', max_length=50, blank=True
    )

    items_total = models.DecimalField(
        'Товары, ₽', max_digits=9, decimal_places=2
    )
    shipping_price = models.DecimalField(
        'Доставка, ₽', max_digits=9, decimal_places=2
    )
    total = models.DecimalField('Итого, ₽', max_digits=9, decimal_places=2)

    status = models.CharField(
        'Статус', max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    paid_at = models.DateTimeField('Оплачен', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.pk}'

    def mark_paid(self):
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])


class OrderItem(models.Model):
    """Снимок позиции на момент заказа: цены и тексты не меняются, даже если товар потом поменяют."""

    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )
    title = models.CharField('Товар', max_length=200)
    variant = models.CharField(
        'Вариант', max_length=20, choices=Variant.choices
    )
    text = models.TextField('Текст', blank=True)
    custom_image = models.ImageField(
        'Картинка клиента', upload_to='custom/', blank=True
    )
    unit_price = models.DecimalField(
        'Цена за шт., ₽', max_digits=8, decimal_places=2
    )
    quantity = models.PositiveSmallIntegerField('Кол-во')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    @property
    def line_total(self):
        return self.unit_price * self.quantity
