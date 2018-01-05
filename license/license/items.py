# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LicenseItem(scrapy.Item):
    license_number = scrapy.Field()
    name = scrapy.Field()
    license_type = scrapy.Field()
    primary_status = scrapy.Field()
    previous_names = scrapy.Field()
    address = scrapy.Field()
    issuance_date = scrapy.Field()
    expiration_date = scrapy.Field()
    current_date_time = scrapy.Field()
    source_url = scrapy.Field()

    rank = scrapy.Field()
    status = scrapy.Field()
    county = scrapy.Field()

