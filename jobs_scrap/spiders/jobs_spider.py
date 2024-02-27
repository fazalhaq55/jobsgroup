import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jobs_scrap.items import JobsScrapItem

class JobsSpiderSpider(CrawlSpider):    
    name = 'jobs_spider'
    start_urls = ['https://www.bayt.com/en/saudi-arabia/jobs']
    allowed_domains = ['bayt.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.bayt.com/en/saudi-arabia/jobs/',body=None, encoding='utf-8', headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//div[@id='results_inner_card']/ul/li[@class='has-pointer-d']//div[@class='p20r u-stretch']//a"), callback="parse_request", follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths="//div[@id='sectionPagination']/ul[@id='pagination']/li/a")
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
        item['job_title'] = response.xpath("//div[@class='t-left']/h1[@id='job_title']/text()").get()
        item['city'] = response.xpath("//ul[@class='media-list is-spaced t-small row']//span[@class='t-mute']/a[@class='t-mute']/span[1]/text()").get()
        work_from_home_text = response.xpath("//div[@class='m10b'][1]//b[@class='t-small']/span/text()").get()

        if work_from_home_text:
            item['work_from_home'] = True
        else:
            item['work_from_home'] = False

        if response.xpath("//ul[@class='media-list is-spaced t-small row']//ul/li/a[@class='is-black t-bold']/span[1]/text()"):
            item['organzation'] = response.xpath("//ul[@class='media-list is-spaced t-small row']//ul/li/a[@class='is-black t-bold']/span[1]/text()").get()
        else:
            item['organzation'] = response.xpath("//ul[@class='media-list is-spaced t-small row']//ul/li[1]/text()").get()

        item['close_date'] = response.xpath("//div[@class='t-small t-mute m10b']/span[2]/text()").get()
        item['job_location'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[1]/dd/text()").get()
        item['company_industry'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[2]/dd/text()").get()
        item['company_type'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[3]/dd/text()").get()
        
        if 'Job Role' in response.xpath("normalize-space(//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[4]/dt/text())").get():
            item['category'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[4]/dd/text()").get()
            item['emp_type'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[5]/dd/text()").get()
            item['salary'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[6]/dd/text()").get()
            no_of_job = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[7]/dd/text()").get()
            if no_of_job is not None and 'Unspecified' in no_of_job:
                item['no_of_jobs'] = 0
            else:
                item['no_of_jobs'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[7]/dd/text()").get()
        else:
            item['category'] = ''
            item['emp_type'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[4]/dd/text()").get()
            item['salary'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[5]/dd/text()").get()
            no_of_job = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[7]/dd/text()").get()
            if no_of_job is not None and 'Unspecified' in no_of_job:
                item['no_of_jobs'] = 0
            else:
                item['no_of_jobs'] = response.xpath("//div[@class='card-content is-spaced p20t']//dl[@class='dlist is-spaced is-fitted t-small']/div[7]/dd/text()").get()
        
            
        item['job_descriptions'] = response.xpath("//div[@class='card u-shadow'][2]//div[@class='t-break']/child::node()").getall()
        item['job_requirements'] = response.xpath("//div[@class='card-content is-spaced t-break print-break-before p20t']/child::node()").getall()
        
        # item['submission_guidelines'] = response.xpath("//div[@class='col-lg-12 row'][9]/child::node()").getall()
        item['submission_email'] = response.xpath("//div[@id='applyButton']/span/a/@href").get()

        yield item
        

   
       