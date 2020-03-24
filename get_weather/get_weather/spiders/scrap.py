import scrapy
from ..items import GetWeatherItem


class MySpider(scrapy.Spider):
    name = "weather_spider"
    start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

    def parse(self, response):
        items = GetWeatherItem()
        values = response.css('div.values')

        for item in values:
            night_temperature = item.css('div.value.span.unit.unit_temperature_c::text').extract()
            day_temperature = item.css('div.value.span.unit.unit_temperature_c::text').extract()

            items['night_temperature'] = night_temperature
            items['day_temperature'] = day_temperature

            yield items
