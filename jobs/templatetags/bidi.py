from django import template

register = template.Library()

@register.filter
def bidi(value):
    if '\u0600' <= value <= '\u06FF':
        # If text contains Arabic characters
        return 'rtl'
    else:
        # Otherwise, assume text is in English and show LTR
        return 'ltr'