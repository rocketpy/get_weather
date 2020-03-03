# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class GetWeatherItem(scrapy.Item):
    night_temperature = scrapy.Field()
    day_temperature = scrapy.Field()

