from django.core.management.base import BaseCommand

from merch.models import Product


class Command(BaseCommand):
    help = 'Создаёт или обновляет базовые товары: открытку А6 и постер А4'

    def handle(self, *args, **options):
        items = [
            {
                'slug': 'otkrytka',
                'title': 'Открытка',
                'kind': Product.Kind.POSTCARD,
                'size': 'А6',
                'price_standard': 110,
                'price_custom': 220,
                'description': 'Стандарт: картинка наша, текст пишете вы.\nСвоя картинка: и картинку, и текст выбираете вы.',
            },
            {
                'slug': 'poster',
                'title': 'Постер',
                'kind': Product.Kind.POSTER,
                'size': 'А4',
                'price_standard': 330,
                'price_custom': 440,
                'description': 'Стандарт: наша картинка.\nСвоя картинка: печатаем ваше изображение.',
            },
        ]
        for data in items:
            slug = data.pop('slug')
            obj, created = Product.objects.update_or_create(
                slug=slug, defaults=data
            )
            self.stdout.write(
                f'{"Создан" if created else "Обновлён"}: {obj.title}'
            )
