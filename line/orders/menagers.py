from django.db import models
from django.db.models.query import QuerySet


class OrderManager(models.Manager):

    def get_order_by_id(self, user_id: int) -> QuerySet:
        return self.filter(user_id=user_id)
