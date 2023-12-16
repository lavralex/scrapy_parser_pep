import re

import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import DOMAIN, SPIDER_NAME


class PepSpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = [DOMAIN]
    start_urls = [f'https://{DOMAIN}/']

    def parse(self, response):
        links = response.xpath(
            '//section[@id="numerical-index"]//a/@href'
        ).extract()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.xpath(
            '//h1[contains(@class,"page-title")]/text()'
        ).get()
        pattern = re.compile(
            r'^PEP\s(?P<number>\d+)\s–\s(?P<name>.*)'
        )
        title_information = pattern.search(title)
        yield PepParseItem({
            'number': title_information.group('number'),
            'name': title_information.group('name').strip(),
            'status': response.xpath(
                '//dt[contains(text(),"Status")]/'
                'following-sibling::dd/abbr/text()'
            ).get()
        })
