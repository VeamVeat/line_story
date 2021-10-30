from django.db import models


class PersonQuerySet(models.QuerySet):
    def w_b(self):
        return self.filter(name='BLACK_AND_WHITE')

    def colored(self):
        return self.filter(name='COLORED')
