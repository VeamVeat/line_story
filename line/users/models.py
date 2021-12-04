from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

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
    @admin.display(
        ordering=_('last_name'),
        description=_('Full name of the user'),
    )
    def full_name(self):
        return self.first_name + ' ' + self.last_name


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
    region = models.CharField(max_length=255, verbose_name=_('region of residence'))
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=False,
                                unique=True)

    image = models.OneToOneField(File, null=True, blank=True, on_delete=models.SET_NULL,
                              verbose_name=_('profile photo'))

    class Meta:
        ordering = ('age',)

    def __str__(self):
        return f'{self.user}'

    @property
    def balance_user(self):
        return self.user.wallet.ballance


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_('amount'), default=0, validators=[MinValueValidator(0)])
    descriptions = models.CharField(max_length=255, verbose_name=_('transaction description'))
    datetime = models.DateTimeField(_('date'), default=timezone.now)

    def __str__(self):
        return f'{self.amount}'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='wallet', verbose_name=_('user`s wallet'))
    ballance = models.PositiveIntegerField(verbose_name=_('user balance'), default=0)

    class Meta:
        unique_together = (("user", "id"),)
        permissions = (("can_add_money", "top up balance"),)

    def queryset(self, db):
        return self.__class__.objects.using(db).filter(id=self.id)

    def increase_balance(self, value, db='default'):
        with transaction.atomic(using=db):
            Transaction.objects.create(user=self.user,
                                       descriptions=f"пополнение счёта на самму {value} "
                                                    f"от пользователя {self.user.email}",
                                       amount=value)
            wallet = self.queryset(db).select_for_update().get()
            wallet.ballance += value
            wallet.save()

    def decrease_balance(self, value, db='default'):
        with transaction.atomic(using=db):
            Transaction.objects.create(user=self,
                                       descriptions=f"списание счёта на самму {value} от пользователя {self.email}",
                                       amount=value)
            wallet = self.queryset(db).select_for_update().get()
            wallet.ballance -= value
            wallet.save()

    def __str__(self):
        return f'{self.ballance}'


@receiver(post_save, sender=User)
def create_profile_and_wallet(sender, instance, created, **kwargs):
    if created:
        file = File.objects.create(image='users/photo_profile/default.jpg')
        Profile.objects.create(user=instance, image=file)
        Wallet.objects.create(user=instance)
        Cart.objects.create(user=instance)
