from django.shortcuts import redirect
from django.views import View

from products.models import ProductFile


class DeleteProductFile(View):
    permission_required = ['change_profile']

    @staticmethod
    def get(request, object_id, objects_product_id):
        if request.user.is_superuser:
            ProductFile.objects.filter(pk=object_id).delete()
        return redirect(f'/admin/products/product/{objects_product_id}/change/')
