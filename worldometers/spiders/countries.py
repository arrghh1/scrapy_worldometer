# -*- coding: utf-8 -*-
import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #firstly, remove the pass, as we're going to send stuff back. Use the xpaths we saw earlier by investigating the site
        countries = response.xpath("//td/a")
        for country in countries:
                name = country.xpath(".//text()").get() #selected object, and not response object, so requires a period at the start
                link = country.xpath(".//@href").get()

        #secondly, we want to make sure we pass an object back (ticker?)
                #absolute_url = response.urljoin(link) # this works becaquse it knows the domain already. f"https://www.worldometers.info{link}"
                yield response.follow(url=link, callback=self.parse_country)

    def parse_country(self, response):
        logging.info(response.url)
