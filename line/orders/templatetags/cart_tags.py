from django import template

register = template.Library()


@register.simple_tag
def total_quantity(price_product, quantity_in_cart_item):
    total_price = price_product * quantity_in_cart_item
    return total_price
