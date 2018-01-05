from twisted.internet import reactor

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from license.spiders.dca_spider import DCASpider

import argparse

def run_spider(boardCode="100", licenseType = "1002", licenseNumber = "", \
                        busName="", firstName="", lastName="", filename="result.json"):
    settings = get_project_settings()
    settings.overrides['FEED_FORMAT'] = 'json'
    settings.overrides['FEED_URI'] = filename

    crawler = CrawlerProcess(settings)
    crawler.crawl(DCASpider, boardCode=boardCode, licenseType=licenseType, licenseNumber=licenseNumber, \
                        busName=busName, firstName=firstName, lastName=lastName)
    crawler.start()

if __name__ == '__main__':
    # define parser to parse arguments from command line input.
    parser = argparse.ArgumentParser(prog='PROG', usage='python start.py boardCode [--type licenseType] [--number licenseNumber] [--bus busName] [--first firstName] [--last lastName] [--file filename]')

    # define argument fields
    parser.add_argument('params', nargs='+', help='input board code & license type')	
    parser.add_argument('--type', nargs='?', help='license type', dest="licenseType")
    parser.add_argument('--number', nargs='?', help='license number', dest="licenseNumber")
    parser.add_argument('--bus', nargs='?', help='business name', dest="busName")
    parser.add_argument('--first', nargs='?', help='first name', dest="firstName")
    parser.add_argument('--last', nargs='?', help='last name', dest="lastName")
    parser.add_argument('--file', nargs='?', help='last name', dest="filename")

    args = parser.parse_args()
    boardCode = args.params[0]

    licenseType = args.licenseType if args.licenseType else ''
    licenseNumber = args.licenseNumber if args.licenseNumber else ''
    busName = args.busName if args.busName else ''
    firstName = args.firstName if args.firstName else ''
    lastName = args.lastName if args.lastName else ''
    filename = args.filename if args.filename else 'result.json'

    run_spider(boardCode, licenseType, licenseNumber, busName, firstName, lastName, filename)
