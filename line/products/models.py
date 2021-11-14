import datetime

from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mixins import CreatedAtMixin


class PersonQuerySet(models.QuerySet):
    def black_and_white(self):
        return self.filter(name=ProductType.Color.W_B)

    def colored(self):
        return self.filter(name=ProductType.Color.COLORED)


class ProductType(models.Model):

    class Color(models.TextChoices):
        W_B = 'BLACK_AND_WHITE', _('BLACK_AND_WHITE')
        COLORED = 'COLORED', _('COLORED')

    name = models.CharField(max_length=15, choices=Color.choices, verbose_name=_('name of product'))

    objects = PersonQuerySet.as_manager()

    class Meta:
        verbose_name = _('type of product')
        verbose_name_plural = _('type of products')

    def __str__(self):
        return self.name


def get_path_file(instance, filename):
    return '/'.join([str(instance.__name__), filename])


class File(models.Model):
    class Type(models.TextChoices):
        JPG = 'jpg'
        PNG = 'png'

    type = models.CharField(max_length=10, choices=Type.choices, verbose_name=_('type of file'))
    file = models.ImageField(default='default image', upload_to=get_path_file)
    size = models.IntegerField(default=0, verbose_name=_('size of file'))
    name = models.CharField(max_length=30, verbose_name=_('name of file'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.name


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Product(CreatedAtMixin):
    type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(null=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_('name of product'))
    description = models.TextField(verbose_name=_('name of description'))
    file = models.ForeignKey(File, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name=_('product photo'))
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))], verbose_name=_('price of product'))
    year_issue = models.IntegerField(db_index=True, validators=[MinValueValidator(2020), max_value_current_year],
                                     verbose_name=_('year of product release'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        unique_together = ('type', 'file',)

    def __str__(self):
        return self.title
