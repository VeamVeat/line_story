from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import JSONField
from django.utils.translation import ugettext_lazy as _

from utils.mixins import CreatedAtMixin
from line import settings
from orders.managers import CartItemManager


class Order(CreatedAtMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, unique=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('number of products in the order'))
    final_price = models.DecimalField(max_digits=12, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.01'))],
                                      verbose_name=_('total order price'))
    product_list = JSONField()
    address = models.CharField(max_length=1800, verbose_name=_('address'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('active order'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey("products.Product", null=True, on_delete=models.SET_NULL, related_name='+')
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity of product in the cart'))
    address = models.CharField(max_length=1800, null=True, blank=True, verbose_name=_('delivery address'))

    objects = CartItemManager()

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('carts items')

    def __str__(self):
        return self.user.email
