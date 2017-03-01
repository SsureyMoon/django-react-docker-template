from django import template

register = template.Library()


@register.filter
def attr_lookup(instance, attr_name):
    try:
        return getattr(instance, attr_name)
    except:
        return None