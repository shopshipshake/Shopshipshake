from django import template
import math
register = template.Library()


@register.filter(is_safe=False)
def number_step(decimal_places):
    """根据decimal_places小数位数返回input的step值"""
    try:
        return 1/math.pow(10, decimal_places)
    except Exception as e:
        return ''