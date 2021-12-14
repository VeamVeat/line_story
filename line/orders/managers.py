from django.db import models


class CartItemManager(models.Manager):
    def get_all_product_in_cart(self, user):
        return self.filter(user=user).prefetch_related('product_set')

    def get_product(self, size):
        return self.filter(size__lt=size)
