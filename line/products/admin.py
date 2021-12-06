from django.contrib import admin
from django.urls import path

from products.forms import ProductAdminForm
from products.models import Product, ProductType, ProductFile
from products.views import DeleteProductFile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price',
                    'year', 'created_at', 'type')

    list_filter = ('title', 'price', 'year')
    radio_fields = {"type": admin.VERTICAL}
    search_fields = ('title', 'price', 'year')
    prepopulated_fields = {'slug': ('title',)}

    form = ProductAdminForm

    change_form_template = 'admin/products/custom_change_form.html'

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'price', 'year',
                       'type', 'product_type', 'image', 'description'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['image']:
            file = form.cleaned_data['image']
            ProductFile.objects.create(product_id=obj.id, image=file)
        if form.cleaned_data['product_type']:
            product_type = form.cleaned_data['product_type']
            product_type_object = ProductType.objects.create(name=product_type)
            Product.objects.filter(id=obj.id).update(type=product_type_object)
        return super(ProductAdmin, self).save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        all_product_photo = ProductFile.objects.filter(product_id=object_id)

        if extra_context is None:
            extra_context = {"all_photo_product": all_product_photo}
        return super(ProductAdmin, self).change_view(
            request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<pk>/<int:product_id>',
                 self.admin_site.admin_view(DeleteProductFile.as_view()),
                 name='delete_product_photo'),
        ]
        return my_urls + urls
