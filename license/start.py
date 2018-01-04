from twisted.internet import reactor

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from license.spiders.dca_spider import DCASpider

def run_spider(boardCode="100", licenseType = "1002", licenseNumber = "", \
                        busName="", firstName="", lastName=""):
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(DCASpider, boardCode=boardCode, licenseType=licenseType, licenseNumber=licenseNumber, \
                        busName=busName, firstName=firstName, lastName=lastName)
    crawler.start()
