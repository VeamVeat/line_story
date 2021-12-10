from decimal import Decimal

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models

from utils.mixins import CreatedAtMixin
from utils.helpers import convert_from_megabyte_to_kilobyte
from line import settings


class ProductType(models.Model):

    name = models.CharField(max_length=255, verbose_name=_('name of product'))

    class Meta:
        verbose_name = _('type of product')
        verbose_name_plural = _('type of products')

    def __str__(self):
        return self.name


def get_path_file(instance, filename):
    return '/'.join([str(instance.name), filename])


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    kilo_byte = convert_from_megabyte_to_kilobyte(settings.MEGA_BYTE_LIMIT)
    if file_size > kilo_byte:
        raise ValidationError("Max file size is %sMB" % str(settings.MEGA_BYTE_LIMIT))


class File(models.Model):
    type = models.CharField(max_length=255, verbose_name=_('type of file'))
    image = models.ImageField(validators=[validate_image], upload_to=get_path_file)
    size = models.IntegerField(default=0, verbose_name=_('size of file'))
    name = models.CharField(max_length=255, verbose_name=_('name of file'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def save(self, *args, **kwargs):
        self.size = self.image.size
        self.name, self.type = self.image.name.split('.')
        super(File, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(CreatedAtMixin):
    type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(null=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_('name of product'))
    description = models.TextField(verbose_name=_('name of description'))
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))], verbose_name=_('price of product'))
    year = models.IntegerField(db_index=True, verbose_name=_('year of product release'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title


class ProductFile(File):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_file')
