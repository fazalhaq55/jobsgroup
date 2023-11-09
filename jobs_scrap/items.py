# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from jobs.models import Info
class JobsScrapItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Info



