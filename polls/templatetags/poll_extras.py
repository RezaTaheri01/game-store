from django import template
from django.utils.text import Truncator
from jalali_date import date2jalali

register = template.Library()


@register.filter(name='cut')  # way 1
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")


@register.filter(name='jalali_date_custom')
def jalali_converter(value):
    return date2jalali(value)


@register.filter(name='sort_by')
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


# register.filter("cut", cut)  # way 2

@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter(name='int_comma')
def three_digits_currency(value: int):
    return '{:,}'.format(value)

