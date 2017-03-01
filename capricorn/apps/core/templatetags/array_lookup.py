from django import template

register = template.Library()


@register.filter
def array_lookup(array, key):
    return array[key]