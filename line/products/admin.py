from django.contrib import admin
from django.urls import path
from django.utils.translation import ugettext_lazy as _

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
    actions = ["set_quantity_zero", ]
    prepopulated_fields = {'slug': ('title',)}

    form = ProductAdminForm

    change_form_template = 'admin/products/custom_change_form.html'

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'price', 'year',
                       'type', 'image', 'description'),
        }),
    )

    @admin.action(description=_('reset the number of selected products'))
    def set_quantity_zero(self, request, queryset):
        for product in queryset:
            product.quantity = 0
            product.save()

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['image'] and request.user.is_superuser:
            file = form.cleaned_data['image']
            ProductFile.objects.create(product_id=obj.id, image=file)
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
            path('<path:object_id>/<path:objects_product_id>/product_photo/',
                 self.admin_site.admin_view(DeleteProductFile.as_view()),
                 name='product_photo'),
        ]
        return my_urls + urls
