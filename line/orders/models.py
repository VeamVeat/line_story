from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from products.models import Product
from orders.menagers import OrderManager
from mixins import CreatedAtMixin

User = get_user_model()


class Order(CreatedAtMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('number of products in the order'))
    final_price = models.DecimalField(max_digits=12, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.01'))],
                                      verbose_name=_('total order price'))
    product_list = JSONField()

    object = OrderManager()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return self.user
