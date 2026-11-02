from django.db import models
from django.urls import reverse


class Variant(models.TextChoices):
    STANDARD = 'standard', 'Стандарт'
    CUSTOM = 'custom', 'Своя картинка'


class Product(models.Model):
    class Kind(models.TextChoices):
        POSTCARD = 'postcard', 'Открытка'
        POSTER = 'poster', 'Постер'

    title = models.CharField('Название', max_length=150)
    slug = models.SlugField('Слаг (для ссылки)', unique=True)
    kind = models.CharField('Тип', max_length=20, choices=Kind.choices)
    description = models.TextField('Описание', blank=True)
    size = models.CharField('Формат', max_length=50, blank=True)
    price_standard = models.DecimalField(
        'Цена: стандарт, ₽', max_digits=8, decimal_places=2, default=0
    )
    price_custom = models.DecimalField(
        'Цена: своя картинка, ₽', max_digits=8, decimal_places=2, default=0
    )
    image = models.ImageField(
        'Стандартное изображение', upload_to='products/', blank=True
    )
    is_active = models.BooleanField('Показывать на сайте', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('merch:detail', args=[self.slug])

    @property
    def allows_text(self):
        return self.kind == self.Kind.POSTCARD

    def price_for(self, variant):
        return (
            self.price_custom
            if variant == Variant.CUSTOM
            else self.price_standard
        )
