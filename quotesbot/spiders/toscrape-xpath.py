# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    urls = [
        'https://scm.hue.workslan/users/sign_in',
        'http://product-ci/users/sign_in'
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.login, dont_filter=True)

    def login(self, response):
        self.log("Login start:")
        self.log(response.body)
        authenticity_token= response.xpath("//meta[@name='csrf-token']/@content")[0].extract()
        print 'token:'+authenticity_token
        frmdata={'utf8': '✓', 'authenticity_token': authenticity_token, 'user[login]': 'song_ji@worksap.co.jp',
                 'user[password]': 'ben321ben', 'user[remenber_me]': '0'}
        yield scrapy.FormRequest(url=response.url, callback=self.parse_gitlab, formdata=frmdata)

    def parse_gitlab(self, response):
        print response.body


    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

