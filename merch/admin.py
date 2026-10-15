from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'price', 'is_customizable', 'is_active')
    list_filter = ('kind', 'is_active', 'is_customizable')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
