from django import template
from django.utils.encoding import force_str
from django.utils import timezone as tz
from datetime import datetime
from jobs.models import Info
import re
register = template.Library()

@register.filter
def replace_string(value):
    if value:
        return value.replace("Position Title:","")
    else:
        pass

@register.filter
def encode(value):
    encoded_data = force_str(value, encoding='utf-8')
    return encoded_data
    
@register.filter
def bidi(value):
    arabic_pattern = re.compile('[\u0600-\u06FF]+')
    persian_pattern = re.compile('[\u0621-\u06FF]+')
    
    if arabic_pattern.search(value) or persian_pattern.search(value):
        return 'rtl'
    else:
        return 'ltr'    

@register.filter
def split(value):
    return value.split(',')

# @register.filter
# def style(value):
#     arabic_pattern = re.compile('[\u0600-\u06FF]+')
#     persian_pattern = re.compile('[\u0621-\u06FF]+')
    
#     if arabic_pattern.search(value) or persian_pattern.search(value):
#         return 'Bahij'
#     else:
#         return 'arial'
        
