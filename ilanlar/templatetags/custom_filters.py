from django import template
import random

register = template.Library()

@register.simple_tag
def random_int(a, b):
    return random.randint(a, b)