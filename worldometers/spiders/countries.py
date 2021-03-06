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
                yield response.follow(url=link, callback=self.parse_country, meta={'country_name':name})

    def parse_country(self, response):
        name = response.request.meta['country_name'] #gets the meta from the other parse function
        rows = response.xpath(f"(//table[contains(@class,'table-list')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'country_name':name,
                'year':year,
                'population':population
            }
