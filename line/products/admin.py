from django.contrib import admin

from products.models import Product, ProductType


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    list_filter = ('name',)

    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'year', 'created_at')

    list_filter = ('title', 'price', 'year')

    search_fields = ('title', 'price', 'year')


