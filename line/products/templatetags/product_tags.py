from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter
def is_false(arg):
    return arg is False


@register.filter
def is_none(arg):
    return arg is None


@register.simple_tag
def product_is_reserved(queryset, user):
    try:
        qr = queryset.get(user=user, is_reserved=True).is_reserved
    except ObjectDoesNotExist:
        qr = False
        return qr
    return qr


@register.simple_tag
def reserved_product_quantity(queryset, user):
    qu = queryset.get(user=user, is_reserved=True).quantity
    return qu
