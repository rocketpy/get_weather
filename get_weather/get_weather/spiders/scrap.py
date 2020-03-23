import scrapy
from ..items import GetWeatherItem


class MySpider(scrapy.Spider):
    name = "weather_spider"
    start_urls = ['http://www.gismeteo.ua/city/daily/5093/']

    def parse(self, response):
        items = GetWeatherItem()
        # values = response.css('div.values')
        # for i in values:
        night_temperature = response.css('span.unit unit_temperature_c::text')[0].extract()
        day_temperature = response.css('span.unit unit_temperature_c::text')[1].extract()
        items['night_temperature'] = night_temperature
        items['day_temperature'] = day_temperature

        yield {'day_temperature': day_temperature, 'night_temperature': night_temperature}
