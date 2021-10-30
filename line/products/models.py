from django.db import models
from django.utils.translation import ugettext_lazy as _

from mixins import TimeMixin
from products.menagers import PersonQuerySet


class ProductType(models.Model):
    W_B = _('BLACK_AND_WHITE')
    COLORED = _('COLORED')

    COLOR_CHOICES = (
        (W_B, _('BLACK_AND_WHITE')),
        (COLORED, _('COLORED'))
    )

    name = models.CharField(max_length=15, choices=COLOR_CHOICES, verbose_name=_('name of product'))

    product_type = PersonQuerySet.as_manager()

    class Meta:
        verbose_name = _('type of product')
        verbose_name_plural = _('type of products')

    def __str__(self):
        return self.name


class File(models.Model):
    JPG = 'jpg'
    PNG = 'png'

    FILE_TYPE_CHOICES = (
        (JPG, 'jpg'),
        (PNG, 'png')
    )

    type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, verbose_name=_('type of file'))
    file = models.ImageField(
        upload_to=lambda instance, filename: '/'.join(['users', 'product', str(instance.type), filename])
    )

    size = models.CharField(max_length=10, verbose_name=_('size of file'))
    name = models.CharField(max_length=10, verbose_name=_('name of file'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.name


class Product(TimeMixin):
    product_type = models.ForeignKey(ProductType, models.CASCADE)
    slug = models.SlugField(null=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_('name of product'))
    description = models.TextField(verbose_name=_('name of description'), null=True)
    file = models.ForeignKey(File, models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('price of product'))
    year_issue = models.DateTimeField(db_index=True, verbose_name=_('year of product release'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        unique_together = ('product_type ', 'file',)

    def __str__(self):
        return self.title

