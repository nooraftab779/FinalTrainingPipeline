from django import template

register = template.Library()

@register.filter(name='lookup', is_safe=True)
def lookup(d, arg):
    return d[arg]