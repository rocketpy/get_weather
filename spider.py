import scrapy
from scrapy.crawler import CrawlerProcess


def show_weather():
    night_temperature = []
    day_temperature = []

    class MySpider(scrapy.Spider):
        name = "weather_spider"
        allowed_domains = ['gismeteo.ua']
        start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

        def parse(self, response):
            values = response.css('div.value')
            night_temp = values.css('span.unit.unit_temperature_c::text')[0].extract()
            day_temp = values.css('span.unit.unit_temperature_c::text')[1].extract()

            night_temperature.append(night_temp)
            day_temperature.append(day_temp)

    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(MySpider)
    process.start()

    print(night_temperature[-1])
    print(day_temperature[-1])

if __name__ == '__main__':
    show_weather()
