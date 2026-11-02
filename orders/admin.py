from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = (
        'product',
        'title',
        'variant',
        'text',
        'custom_image',
        'unit_price',
        'quantity',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'total',
        'status',
        'created_at',
    )
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = (
        'token',
        'user',
        'items_total',
        'shipping_price',
        'total',
        'created_at',
        'paid_at',
    )
    inlines = [OrderItemInline]
