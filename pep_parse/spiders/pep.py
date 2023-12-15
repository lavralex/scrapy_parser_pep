import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        links = response.xpath(
            '//section[@id="numerical-index"]//a/@href'
        ).extract()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.xpath('//h1[contains(@class,"page-title")]/text()').get()
        pattern = re.compile(r'^PEP\s(?P<number>\d+)\s–\s(?P<name>.*)')
        title_information = pattern.search(title)
        yield PepParseItem({
            'number': title_information.group('number'),
            'name': title_information.group('name').strip().replace('\n', '').replace('\r', ''),
            'status': response.xpath(
                '//dt[contains(text(),"Status")]/'
                'following-sibling::dd/abbr/text()'
            ).get()
        })
