from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ProductManager(models.Manager):
    def get_product_files(self, object_id):
        try:
            return self.get(id=object_id).prefetch_related('product_file')
        except ObjectDoesNotExist:
            return None

