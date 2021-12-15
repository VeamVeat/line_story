from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class CartItemManager(models.Manager):
    def get_all_product_in_cart(self, user):
        return self.filter(user=user).prefetch_related('product_set')

