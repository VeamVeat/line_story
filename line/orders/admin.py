from django.contrib import admin
from orders.models import Order, Cart


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'quantity', 'final_price', 'list_product')

    list_filter = ('final_price',)

    search_fields = ('final_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'product')

    list_filter = ('quantity',)

    search_fields = ('product',)


