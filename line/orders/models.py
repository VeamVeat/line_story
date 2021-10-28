from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

from line.settings import AUTH_USER_MODEL
from products.models import Product, TimedModel


class Order(TimedModel):
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    quantity = models.IntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая стоимость заказа")
    list_product = JSONField()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        unique_together = ('user ', 'file ',)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    quantity = models.IntegerField(default=1)
    product = models.ManyToManyField(Product, models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.user
