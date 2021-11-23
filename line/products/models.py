from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.mixins import CreatedAtMixin


class ProductType(models.Model):

    name = models.CharField(max_length=255, verbose_name=_('name of product'))

    class Meta:
        verbose_name = _('type of product')
        verbose_name_plural = _('type of products')

    def __str__(self):
        return self.name


def get_path_file(instance, filename):
    return '/'.join([str(instance.name), filename])


class File(models.Model):
    type = models.CharField(max_length=255, verbose_name=_('type of file'))
    file = models.ImageField(upload_to=get_path_file)
    size = models.IntegerField(default=0, verbose_name=_('size of file'))
    name = models.CharField(max_length=255, verbose_name=_('name of file'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.name


class Product(CreatedAtMixin):
    type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(null=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_('name of product'))
    description = models.TextField(verbose_name=_('name of description'))
    file = models.ForeignKey(File, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name=_('product photo'))
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))], verbose_name=_('price of product'))
    year = models.IntegerField(db_index=True, verbose_name=_('year of product release'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        unique_together = ('type', 'file',)

    def __str__(self):
        return self.title
