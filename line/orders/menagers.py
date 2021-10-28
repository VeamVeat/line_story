from django.db import models
from django.db.models.query import QuerySet


class OrderManager(models.Manager):

    def find_all_for(self, user_id: int) -> QuerySet:
        queryset = self.get_queryset()
        return queryset.filter(user_id=user_id)
