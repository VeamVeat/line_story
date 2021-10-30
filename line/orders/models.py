from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from products.models import Product
from orders.menagers import OrderManager
from mixins import TimeMixin


class Order(TimeMixin):
    user = models.ForeignKey(get_user_model, models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    quantity = models.IntegerField(default=1, verbose_name=_('number of products in the order'))
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="total order price")
    list_product = JSONField()

    object = OrderManager()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        unique_together = ('user',)


class Cart(models.Model):
    user = models.ForeignKey(get_user_model, models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    quantity = models.IntegerField(default=1, verbose_name=_('number of products in the basket'))
    product = models.ManyToManyField(Product, models.CASCADE)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return self.user
