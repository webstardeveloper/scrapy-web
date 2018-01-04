import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from lxml import html
from license.items import LicenseItem

import time

class DCASpider(scrapy.Spider):
    name = "dca"
    domain = "https://search.dca.ca.gov"

    def __init__(self, boardCode="100", licenseType = "1002", licenseNumber = "", \
                        busName="", firstName="", lastName=""):
        self.driver = webdriver.PhantomJS() # or add to your PATH
        # self.driver.set_window_size(1024, 768) # optional
        self.boardCode = boardCode
        self.licenseType = licenseType
        self.licenseNumber = licenseNumber
        self.busName = busName
        self.firstName = firstName
        self.lastName = lastName

    def start_requests(self):
        self.driver.get('https://search.dca.ca.gov')

        time.sleep(1)
        try:
            Select(self.driver.find_element_by_id('boardCode')).select_by_value(self.boardCode)
        except:
            time.sleep(2)
            self.driver.get('https://search.dca.ca.gov')
            time.sleep(1)
            Select(self.driver.find_element_by_id('boardCode')).select_by_value(self.boardCode)

        Select(self.driver.find_element_by_id('licenseType')).select_by_value(self.licenseType)
        self.driver.find_element_by_id('licenseNumber').send_keys(self.licenseNumber)
        self.driver.find_element_by_id('busName').send_keys(self.busName)
        self.driver.find_element_by_id('firstName').send_keys(self.firstName)
        self.driver.find_element_by_id('lastName').send_keys(self.lastName)
        self.driver.find_element_by_id('srchSubmitHome').click()
        time.sleep(2)

        source = self.driver.page_source.encode("utf8")
        tree = html.fromstring(source)

        detail_list = tree.xpath("//a[@class='button newTab']/@href")
        for url in detail_list:
            if url.strip() == "":
                continue
            yield scrapy.Request(url=self.domain + url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = LicenseItem()

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

        yield item


    def validate(self, xpath_obj):
        try:
            xpath_obj = xpath_obj.extract()
            return xpath_obj[0].strip()
        except:
            return ""