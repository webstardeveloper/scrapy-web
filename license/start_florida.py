from twisted.internet import reactor

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from license.spiders.florida_spider import FloridaSpider

import argparse

def run_spider(licenseCategory="05", licenseType = "0501", \
                    county="22_Columbia", name="", licenseNumber="", filename="result.json"):
    settings = get_project_settings()
    settings.overrides['FEED_FORMAT'] = 'json'
    settings.overrides['FEED_URI'] = filename

    crawler = CrawlerProcess(settings)
    crawler.crawl(FloridaSpider, licenseCategory=licenseCategory, licenseType=licenseType, \
                        county=county, name=name, licenseNumber=licenseNumber)
    crawler.start()

if __name__ == '__main__':
    # define parser to parse arguments from command line input.
    parser = argparse.ArgumentParser(prog='PROG', usage='python start.py boardCode [--type licenseType] [--number licenseNumber] [--bus busName] [--first firstName] [--last lastName] [--file filename]')

    # define argument fields
    parser.add_argument('params', nargs='+', help='input licenseCategory')	
    parser.add_argument('--type', nargs='?', help='license type', dest="licenseType")
    parser.add_argument('--number', nargs='?', help='license number', dest="licenseNumber")
    parser.add_argument('--county', nargs='?', help='county', dest="county")
    parser.add_argument('--name', nargs='?', help='name', dest="name")
    parser.add_argument('--file', nargs='?', help='filename', dest="filename")

    args = parser.parse_args()
    licenseCategory = args.params[0]

    licenseType = args.licenseType if args.licenseType else ''
    licenseNumber = args.licenseNumber if args.licenseNumber else ''
    county = args.county if args.county else '22_Columbia'
    name = args.name if args.name else ''
    filename = args.filename if args.filename else 'result.json'

    run_spider(licenseCategory, licenseType, county, name, licenseNumber, filename)
