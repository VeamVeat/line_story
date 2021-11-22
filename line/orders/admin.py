from django.contrib import admin
from orders.models import Order, Cart


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'final_price', 'product_list')

    list_filter = ('final_price',)

    search_fields = ('final_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

    search_fields = ('product',)


