from django.db import models
from django.contrib.postgres.fields import JSONField

from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    quantity = models.IntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая стоимость заказа")
    list_product = JSONField()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    quantity = models.IntegerField(default=1)
    product = models.ManyToManyField(Product, models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.user

