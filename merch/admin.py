from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'kind',
        'size',
        'price_standard',
        'price_custom',
        'is_active',
    )
    list_filter = ('kind', 'is_active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
