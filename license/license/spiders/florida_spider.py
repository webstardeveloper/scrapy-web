import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from lxml import html
from license.items import LicenseItem

import time

class FloridaSpider(scrapy.Spider):
    name = "florida"
    domain = "https://www.myfloridalicense.com/"

    def __init__(self, licenseCategory="05", licenseType = "0501", \
                        county="22", name="", licenseNumber=""):
        self.driver = webdriver.PhantomJS() # or add to your PATH
        # self.driver.set_window_size(1024, 768) # optional
        self.licenseCategory = licenseCategory
        self.licenseType = licenseType
        self.state = "FL"
        self.county = county
        self.name = name
        self.licenseNumber = licenseNumber

    def start_requests(self):
        self.driver.get('https://www.myfloridalicense.com/wl11.asp?mode=1&SID=&brd=&typ=N')

        time.sleep(1)

        try:
            Select(self.driver.find_element_by_name('Board')).select_by_value(self.licenseCategory)
        except:
            time.sleep(2)
            self.driver.get('https://www.myfloridalicense.com/wl11.asp?mode=1&SID=&brd=&typ=N')
            time.sleep(1)
            Select(self.driver.find_element_by_name('Board')).select_by_value(self.licenseCategory)

        Select(self.driver.find_element_by_name('LicenseType')).select_by_value(self.licenseType)
        Select(self.driver.find_element_by_name('County')).select_by_value(self.county)
        Select(self.driver.find_element_by_name('State')).select_by_value(self.state)
        Select(self.driver.find_element_by_name('RecsPerPage')).select_by_value("50")
        
        self.driver.find_element_by_name('Search1').click()
        time.sleep(2)

        source = self.driver.page_source.encode("utf8")

        total_page = source.split('Page 1 of')[1].strip().split(' ')[0].strip()
        index = 1

        while index >= total_page:
            source = self.driver.page_source.encode("utf8")
            tree = html.fromstring(source)

            detail_list = tree.xpath("//table[@bgcolor='#b6c9dc']//a/@href")
            for url in detail_list:
                if url.strip() == "" or 'LicenseDetail' not in url:
                    continue
                print self.domain + url
            index += 1
            self.driver.find_element_by_name('SearchForward').click()
            # yield scrapy.Request(url=self.domain + url, callback=self.parse_detail)

    def parse_detail(self, response):
        '''item = LicenseItem()

        item['license_number'] = self.validate(response.xpath("//h2[@id='licDetail']/text()")).split(":")[1].strip()
        item['name'] = self.validate(response.xpath("//p[@id='name']/text()"))
        item['license_type'] = self.validate(response.xpath("//p[@id='licType']/text()"))
        item['primary_status'] = self.validate(response.xpath("//p[@id='primaryStatus']/text()"))
        item['previous_names'] = self.validate(response.xpath("//p[@id='prevName']/text()"))
        item['address'] = self.validate(response.xpath("//div[@id='address']//p/text()"))
        item['issuance_date'] = self.validate(response.xpath("//p[@id='issueDate']/text()"))
        item['expiration_date'] = self.validate(response.xpath("//p[@id='expDate']/text()"))
        item['current_date_time'] = " ".join(response.xpath("//div[@class='meta']/p[6]/text()").extract())
        item['source_url'] = response.url

        yield item'''
        pass


    def validate(self, xpath_obj):
        try:
            xpath_obj = xpath_obj.extract()
            return xpath_obj[0].strip()
        except:
            return ""