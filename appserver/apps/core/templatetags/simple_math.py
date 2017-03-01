from django import template

register = template.Library()


@register.filter
def decrement(instance):
    return int(instance)-1

@register.filter
def increment(instance):
    return int(instance)+1
