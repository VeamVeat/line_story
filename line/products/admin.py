from django.contrib import admin

from products.models import Product, ProductType, File


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    list_filter = ('name',)

    search_fields = ('name',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('type', 'file', 'size', 'name')

    list_filter = ('size',)

    search_fields = ('type', 'size')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'year_issue', 'created_at')

    list_filter = ('title', 'price', 'year_issue')

    search_fields = ('title', 'price', 'year_issue')


