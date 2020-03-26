import scrapy
from ..items import GetWeatherItem


class MySpider(scrapy.Spider):
    name = "weather_spider"
    allowed_domains = ['gismeteo.ua']
    start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

    def parse(self, response):
        # items = GetWeatherItem()
        values = response.css('.values')
        for val in values:
            night_temperature = val.css('.unit.unit_temperature_c::text')[0].extract()
            day_temperature = val.css('.unit.unit_temperature_c::text')[1].extract()
            items = GetWeatherItem()
            items['night_temperature'] = night_temperature
            items['day_temperature'] = day_temperature

            yield items
