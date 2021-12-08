from django import template
register = template.Library()


@register.filter
def get_index(indexable, i):
    return indexable[i]
