import scrapy


class MySpider(scrapy.Spider):
    name = "Weather_spider"
    start_urls = ['http://www.gismeteo.ua/city/daily/5093/']

    def parse(self, response):
        for item in response.css('div.values'):
            items = {
                'day temperature': response.css('small.author::text').extract(),
                'night temperature': response.css('span.text::text').extract()
                    }
            yield items

