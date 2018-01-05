import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from lxml import html
from license.items import LicenseItem

import time
import re

class FloridaSpider(scrapy.Spider):
    name = "florida"
    domain = "https://www.myfloridalicense.com/"

    def __init__(self, licenseCategory="05", licenseType = "0501", \
                        county="22_Columbia", name="", licenseNumber=""):
        self.driver = webdriver.PhantomJS() # or add to your PATH
        # self.driver.set_window_size(1024, 768) # optional
        self.licenseCategory = licenseCategory
        self.licenseType = licenseType
        self.state = "FL"
        self.county = county.split("_")[0]
        self.county_label = county.split("_")[1]
        self.name = name
        self.licenseNumber = licenseNumber

        self.urls = []

    def start_requests(self):
        yield scrapy.Request(url=self.domain, callback=self.parse)

    def parse(self, response):
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

        total_page = int(source.split('Page 1 of')[1].strip().split(' ')[0].strip())
        
        index = 1

        while index <= total_page:
            source = self.driver.page_source.encode("utf8")
            tree = html.fromstring(source)

            '''detail_list = tree.xpath("//table[@bgcolor='#b6c9dc']//a/@href")
            for url in detail_list:
                if url.strip() == "" or 'LicenseDetail' not in url:
                    continue
                self.urls.append(self.domain + url)
            index += 1

            print "ppppppppppppppppppppppppppppppp"
            print index'''

            tokens = tree.xpath("//table[@bgcolor='#b6c9dc']//tr[@height='40']")
            for i in range(0, len(tokens), 2):
                item = LicenseItem()

                print self.domain + self.validate1(tokens[i].xpath(".//a/@href"))
                print tokens[i].xpath("./td[4]/font/text()")
                item['name'] = self.validate1(tokens[i].xpath(".//a/text()"))
                item['address'] = self.validate1(tokens[i+1].xpath(".//tr/td[2]/font/text()"))
                item['county'] = self.county_label
                item['license_type'] = self.validate1(tokens[i].xpath("./td[1]/font/text()"))
                try:
                    item['rank'] = tokens[i].xpath("./td[4]/font/text()")[1].strip()
                except:
                    item['rank'] = ""
                item['license_number'] = self.validate1(tokens[i].xpath("./td[4]/font/text()"))
                item['primary_status'] = self.validate1(tokens[i].xpath("./td[5]/font/text()")).replace(",", "")
                item['issuance_date'] = ''
                try:
                    item['expiration_date'] = tokens[i].xpath("./td[5]/font/text()")[1].strip()
                except:
                    item['expiration_date'] = ""
                item['source_url'] = self.domain + self.validate1(tokens[i].xpath(".//a/@href"))

                if self.name != "" and self.name not in item['name']:
                    continue
                if self.licenseNumber != "" and self.licenseNumber != item['license_number']:
                    continue

                yield item

            index += 1
            self.driver.find_element_by_name('Page').send_keys(index)
            self.driver.find_element_by_name('SearchGo').click()
            
        # yield scrapy.Request(url=self.domain, callback=self.parse_detail)
        '''for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)'''

    def parse_detail(self, response):
        pass
        item = LicenseItem()

        attrs = response.xpath("//table[@bgcolor='#e9edf2']//b/text()").extract()
        attrs = [attr.strip() for attr in attrs]
        print attrs

        item['name'] = attrs[0]
        item['address'] = attrs[1] + " " + re.sub(r'[^\x00-\x7f]',r' ',attrs[2])
        item['county'] = attrs[2]
        item['license_type'] = attrs[8]
        item['rank'] = attrs[9]
        item['license_number'] = attrs[10]
        item['primary_status'] = attrs[11]
        item['issuance_date'] = attrs[12]
        item['expiration_date'] = attrs[13]
        item['source_url'] = response.url

        yield item


    def validate(self, xpath_obj):
        try:
            xpath_obj = xpath_obj.extract()
            return xpath_obj[0].strip()
        except:
            return ""

    def validate1(self, xpath_obj):
        try:
            return xpath_obj[0].strip()
        except:
            return ""
