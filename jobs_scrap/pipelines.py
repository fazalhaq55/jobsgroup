# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django.utils.text import slugify
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from jobs.models import Info
from django.db.models import Q
from django.utils import timezone
from bidi.algorithm import get_display
import arabic_reshaper
from unidecode import unidecode
import re

def custom_slugify(text):
# Reshape the Arabic text to properly connect Arabic characters
    reshaped_text = arabic_reshaper.reshape(text)
    # Set the text directionality to right-to-left (RTL)
    bidi_text = get_display(reshaped_text)
    # Convert the Arabic RTL text to English slug
    english_slug = slugify(bidi_text, allow_unicode=True)
    return english_slug

class JobsScrapPipeline(object):


    def process_item(self, item, spider):
        
        persian_pattern = re.compile(r'[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\u200F]+')
        urls = Info.objects.values_list('url', flat=True).filter(~Q(url=None))
        # fetch urls
        for i in urls:
            if item['url'] in i:
                raise DropItem()
            # here we check for url field value in response.url 
            # if exist in db just drop that item
        else:
            
            for i in item['job_title']:
                if persian_pattern.search(i):
                    raise DropItem()
                
            for i in item['job_requirements']:
                if persian_pattern.search(i):
                    raise DropItem()
                
            j = '\t\n'.join(item['job_descriptions'])
            item['job_descriptions'] = j
            j_r = '\t\n'.join(item['job_requirements'])
            item['job_requirements'] = j_r
            a_d = '\t\n'.join(item['About_description'])
            item['About_description'] = a_d
            s_g = '\t\t'.join(item['submission_guidelines'])
            item['submission_guidelines'] = s_g
            j_l = ', '.join(item['job_location'])
            item['job_location'] = j_l

            decoded_job_title = unidecode(item['job_title'])
            slugify_title = slugify(decoded_job_title)
            item['jobs_slug'] = slugify_title   

            slugify_category = slugify(item['category'])
            item['slug_cate'] = slugify_category

            decoded_organization = unidecode(item['organzation'])
            slugify_org = slugify(decoded_organization)
            item['slug_cpn'] = slugify_org

            item['meta_tag'] = item['job_title']
            
            item['activation_date'] = timezone.now()
            item.save()
            return item
