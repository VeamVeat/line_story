from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from users.managers import UserManager
from orders.models import Cart
from products.models import File


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def full_name(self):
        return f"{self.first_name}, {self.last_name}"


def _user_directory_path(instance, filename):
    return f"users/image_profile/user_{instance.user.id}/{filename}"


def validate_age(value):
    min_age = 18

    if value < min_age:
        raise ValidationError(
            _('age must be at least 18.'),
            params={'value': value},
        )


class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_('phone number must not'
                                           ' consist of space and '
                                           'requires country code.'
                                           ' eg : +79546748973'))

    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name=_('phone'))
    age = models.PositiveIntegerField(validators=[validate_age], default=0, verbose_name=_('age'))
    region = models.CharField(max_length=50, verbose_name=_('region of residence'))
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=False,
                                unique=True)

    image = models.OneToOneField(File, on_delete=models.CASCADE, verbose_name=_('profile photo'))


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='wallet', verbose_name=_('user`s wallet'))
    ballance = models.PositiveIntegerField(verbose_name=_('user balance'), default=0)

    class Meta:
        unique_together = (("user", "id"),)
        permissions = (("can_add_money", "top up balance"),)

    def __str__(self):
        return f'{self.ballance}'


@receiver(post_save, sender=User)
def create_profile_and_wallet(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(user=instance)
        Cart.objects.create(user=instance)
