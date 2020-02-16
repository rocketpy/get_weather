import scrapy


class MySpider(scrapy.Spider):
    name = "Weather_spider"
    start_urls = ['http://www.gismeteo.ua/city/daily/5093/']

    def parse(self, response):
        #self.log('I just visited: ' + response.url)
        for item in response.css('div.values'):
            items = {
                'day temperature': item.css('small.author::text').extract_first(),
                'night temperature': item.css('span.text::text').extract_first()
                    }
            yield item
