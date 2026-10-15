from django.db import models
from django.urls import reverse


class Product(models.Model):
    class Kind(models.TextChoices):
        POSTCARD = 'postcard', 'Открытка'
        POSTER = 'poster', 'Постер'

    title = models.CharField('Название', max_length=150)
    slug = models.SlugField('Слаг (для ссылки)', unique=True)
    kind = models.CharField('Тип', max_length=20, choices=Kind.choices)
    description = models.TextField('Описание', blank=True)
    size = models.CharField(
        'Размер', max_length=50, blank=True, help_text='Например: А6, 30×40 см'
    )
    price = models.DecimalField('Цена, ₽', max_digits=8, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True)
    is_customizable = models.BooleanField(
        'Можно кастомизировать', default=False
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
