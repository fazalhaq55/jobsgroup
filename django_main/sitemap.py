from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):

    changefreq = "weekly"
    protocol = 'https'

    def items(self):
        return ['jobs','contact-us','companies','application_form']

    def location(self, item):
        return reverse(item)