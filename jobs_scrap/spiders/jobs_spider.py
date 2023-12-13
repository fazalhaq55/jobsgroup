import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jobs_scrap.items import JobsScrapItem
import time
from jobs.models import Info
import logging
from scrapy import signals, Request
from scrapy.exceptions import DontCloseSpider

class JobsSpiderSpider(CrawlSpider):    
    name = 'jobs_spider'
    start_urls = ['http://www.acbar.org/jobs']
    allowed_domains = ['acbar.org']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://www.acbar.org/jobs',body=None, encoding='utf-8', headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//table[@class="table-bordered"]//tr/td[2]/a'), callback="parse_request", follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//a[@rel="next"]')
        ),
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_request(self, response):
        
        item = JobsScrapItem()
        br = '<br>'
        breakline = ','
        # response = response.replace(body=response.body.replace(br.encode('ascii')))
        item['url'] = response.url
        item['job_title'] = response.xpath("//h2[@class='job-title']/text()").get()
        item['job_location'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr//a/text()").getall() 
        item['nationality'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr[2]/td/text()").get()
        item['category'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr[3]/td/text()").get()
        item['emp_type'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr[4]/td/text()").get()
        item['salary'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr[5]/td/text()").get()
        item['vacancy_number'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr[6]/td/text()").get()
        item['no_of_jobs'] = response.xpath("//div[@class='col-md-6 col-lg-offset-6 pull-left']//tr[7]/td/text()").get()
        # ******************************************************************************************
    
        item['city'] = response.xpath("//div[@class='col-md-6']//tr[1]/td/text()").get()
        item['organzation'] = response.xpath("//div[@class='col-md-6']//tr[2]/td/text()").get()
        item['years_of_experience'] = response.xpath("//div[@class='col-md-6']//tr[3]/td/text()").get()
        item['contract_duration'] = response.xpath("//div[@class='col-md-6']//tr[4]/td/text()").get()
        item['gender'] = response.xpath("//div[@class='col-md-6']//tr[5]/td/text()").get()
        item['education'] = response.xpath("//div[@class='col-md-6']//tr[6]/td/text()").get()
        item['close_date'] = response.xpath("//div[@class='col-md-6']//tr[7]/td/text()").get()

        if response.xpath("//div[@class='col-lg-12 row'][2]/child::node()"):
            item['About_description'] = response.xpath("//div[@class='col-lg-12 row'][3]/child::node()").getall()
        else:
            pass
        if response.xpath("//div[@class='col-lg-12 row'][4]/child::node()"):
            item['job_descriptions'] = response.xpath("//div[@class='col-lg-12 row'][5]/child::node()").getall()
        else:
            pass
        if response.xpath("//div[@class='col-lg-12 row'][6]/child::node()"):
            item['job_requirements'] = response.xpath("//div[@class='col-lg-12 row'][7]/child::node()").getall()
        else:
            pass
        if response.xpath("//div[@class='col-lg-12 row'][8]/child::node()"):
            item['submission_guidelines'] = response.xpath("//div[@class='col-lg-12 row'][9]/child::node()").getall()
        else:
            pass
        if response.xpath("//div[@class='col-lg-12 row'][10]/h3/child::node()"):
            item['submission_email'] = response.xpath("//div[@class='col-lg-12 row'][11]//p/child::node()").get()

        yield item
        

   
       