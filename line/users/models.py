from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from line.settings import AUTH_USER_MODEL


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


def _user_directory_path(instance, filename):
    return 'users/image_profile/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must not consist "
                                         "of space and requires country "
                                         "code. eg : +79546748973")

    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Телефон")
    age = models.PositiveIntegerField(default=0, verbose_name="Возраст")
    region = models.CharField(max_length=50, verbose_name="Регион проживания")
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=False,
                                unique=True)

    image = models.ImageField(
        default='users/image_profile/default.png',
        upload_to=_user_directory_path,
        verbose_name="Фото профиля"
    )

    def __str__(self):
        return 'Profile for user {}'.format(self.user.email)


class WalletModel(models.Model):
    user_id = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='wallet', verbose_name='Кошелёк пользователя')
    ballance = models.PositiveIntegerField(verbose_name='баланс пользователя', default=0)

    class Meta:
        unique_together = (("user_id", "id"),)
        permissions = (("can_add_money", "Top up balance"),)

    def __str__(self):
        return f'{self.user_id.last_name} - {self.ballance}'

    @property
    def full_name(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        WalletModel.objects.create(user_id=instance)
    else:
        try:
            instance.profile.save()
            instance.wallet.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
            WalletModel.objects.create(user_id=instance)


