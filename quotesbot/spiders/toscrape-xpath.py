# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    urls = [
       # 'https://scm.hue.workslan/',
        'http://product-ci/users/sign_in'
    ]

    handle_httpstatus_list = [301, 302]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.login, dont_filter=True)

    def login(self, response):
        authenticity_token= response.xpath("//meta[@name='csrf-token']/@content")[0].extract()
        print 'token:'+authenticity_token
        frmdata = {'utf8': '✓', 'authenticity_token': authenticity_token, 'user[login]': 'song_ji@worksap.co.jp',
                  'user[password]': 'ben321ben', 'user[remenber_me]': '0'}
        return scrapy.FormRequest(url=response.url, callback=self.parse_gitlab, formdata=frmdata, dont_filter=True)

    def parse_gitlab(self, response):
        if 300 <= response.status < 400:
            cookie = response.meta['cookiejar']
            print 'cookie:' + cookie
        else:
            return scrapy.Request(url='product-ci', callback=self.parse, meta={'cookiejar': response.meta['cookiejar']})

    def parse(self, response):
        pass
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

