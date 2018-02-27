from django import template
register = template.Library()


@register.filter
def to_currency(value):
    return "{:03.2f}".format(float(value))
