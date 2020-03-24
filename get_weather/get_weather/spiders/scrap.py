import scrapy
from ..items import GetWeatherItem


class MySpider(scrapy.Spider):
    name = "weather_spider"
    start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

    def parse(self, response):
        items = GetWeatherItem()
        
        items['night_temperature'] = night_temperature
        items['day_temperature'] = day_temperature
        values = response.css('div.values')
        #night_temperature = response.css('div.value.span.unit unit_temperature_c::text')[0].extract()
        #day_temperature = response.css('div.value.span.unit unit_temperature_c::text')[1].extract()

        for item in values:
            night_temperature = item.css('div.value.span.unit unit_temperature_c::text')[0].extract()
            day_temperature = item.css('div.value.span.unit unit_temperature_c::text')[1].extract()

"""
            yield {
                'night_temperature': night_temperature,
                'day_temperature': day_temperature}

"""