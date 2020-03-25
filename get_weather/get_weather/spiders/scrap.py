import scrapy
from ..items import GetWeatherItem


class MySpider(scrapy.Spider):
    name = "weather_spider"
    start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

    def parse(self, response):
        items = GetWeatherItem()
        values = response.css('div.value')


        night_temperature = values.css('span.unit.unit_temperature_c::text')[0].extract()
        day_temperature = values.css('span.unit.unit_temperature_c::text')[1].extract()

        items['night_temperature'] = night_temperature
        items['day_temperature'] = day_temperature

        #yield items
