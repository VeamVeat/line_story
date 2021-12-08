from django.urls import reverse
from django.views.generic import DeleteView

from products.models import ProductFile


class DeleteProductFile(DeleteView):
    model = ProductFile
    permission_required = ['change_profile']

    def get_success_url(self):
        product_id = self.kwargs['product_id']
        return reverse('admin:products_product_change', kwargs={'object_id': product_id})
