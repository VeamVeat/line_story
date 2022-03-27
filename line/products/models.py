from decimal import Decimal
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

from line import settings
from products.managers import ProductManager
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


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    mega_byte_limit = 2.0
    kilo_byte = mega_byte_limit*1024*1024
    if file_size > kilo_byte:
        raise ValidationError("Max file size is %sMB" % str(mega_byte_limit))


# storage = FileSystemStorage(location=STATIC_ROOT, base_url=STATIC_URL)
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

    @property
    def product_image(self):
        return self.image

    def __str__(self):
        return self.name


class Product(CreatedAtMixin):
    type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL, related_name='product')
    slug = models.SlugField(null=False, unique=True)
    title = models.CharField(max_length=255, verbose_name=_('name of product'))
    description = models.TextField(verbose_name=_('name of description'))
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))], verbose_name=_('price of product'))
    year = models.IntegerField(db_index=True, verbose_name=_('year of product release'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('number of products'))

    objects = ProductManager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product', kwargs={'product_slug': self.slug})

    @property
    def get_product_in_the_dict(self):
        product_images = ProductFile.objects.filter(product_id=self.pk)[:1].get()
        product_in_the_dict = {
            "id": self.pk,
            "type": self.type.name,
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "year": self.year,
            "image": product_images.image.url,
            'quantity': self.quantity
        }
        return product_in_the_dict

    @property
    def is_stock(self) -> bool:
        return True if self.quantity > 0 else False


class ProductFile(File):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_file')


@receiver(post_save, sender=Product)
def send_mails(sender, instance, created, **kwargs):
    User = get_user_model()
    all_user = User.objects.all()

    if created:
        subject = 'New Product'
        for user in all_user:
            message = render_to_string('products/new_product_notification.html', {
                'user': user,
                'product': instance.title
            })
            user.email_user(subject, message)

