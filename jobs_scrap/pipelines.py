# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django.utils.text import slugify
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from jobs.models import Info
from django.db.models import Q
import re


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
                
        urls = Info.objects.values_list('url', flat=True).filter(~Q(url=None))
        # fetch urls
        for i in urls:
            if item['url'] in i:
                raise DropItem()
            # here we check for url field value in response.url 
            # if exist in db just drop that item
        else:
            j = '\t\n   '.join(item['job_descriptions'])
            item['job_descriptions'] = j

            jl = ' '.join(item['job_location'].split())
            item['job_location'] = jl

            # org = '\n'.join(item['organzation'])
            # item['organzation'] = org

            # date = '\n  '.join(item['close_date'])
            # UpdatedDate = ' '.join(date.split())
            # item['close_date'] = UpdatedDate

            # occupational_groups = '\n'.join(item['occupational_groups'])
            # item['occupational_groups'] = occupational_groups

            # grade = '\n'.join(item['grade'])
            # item['grade'] = grade

            j_r = '\t\n'.join(item['job_requirements'])
            item['job_requirements'] = j_r

            slugify_title = slugify(item['job_title'],allow_unicode=True)
            item['jobs_slug'] = slugify_title 

            item['meta_tag'] = item['job_title']  

            slugify_category = slugify(item['category'])
            item['slug_cate'] = slugify_category    
            
            slugify_industry = slugify(item['company_industry'])
            item['company_industry_slug'] = slugify_industry

            city_slug = slugify(item['city'])
            item['city_slug'] = city_slug

            company_type_slug = slugify(item['company_type'])
            item['company_type_slug'] = company_type_slug

            emp_type_slug = slugify(item['emp_type'])
            item['emp_type_slug'] = emp_type_slug

            slugify_org = slugify(item['organzation'],allow_unicode=True)
            item['slug_cpn'] = slugify_org

            item.save()
        return item
