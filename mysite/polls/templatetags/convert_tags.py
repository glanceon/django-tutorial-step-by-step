# convert_tags.py
from django import template

register = template.Library()

@register.filter()
def add_quotes(value: str):
    """ Add double quotes to a string value """
    return str(value)