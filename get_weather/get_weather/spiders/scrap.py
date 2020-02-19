import scrapy


class MySpider(scrapy.Spider):
    name = "weather_spider"
    start_urls = ['http://www.gismeteo.ua/city/daily/5093/']

    def parse(self, response):
        for item in response.css('div.values'):
            items = {
                'night temperature': response.css('span.unit unit_temperature_c::text')[0].extract(),
                'day temperature': response.css('span.unit unit_temperature_c::text')[1].extract()
                    }
            yield items


