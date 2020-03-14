# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta

class RadiospisCrawlerSpider(scrapy.Spider):
    name = 'radiospis_crawler'
    allowed_domains = ['radiospis.pl']
    broadcasts = ['rmf-fm', 'zet', 'vox-fm', 'eska', 'muzo-fm', 'trojka']
    _dates = [(datetime.today() - timedelta(days=n)).strftime('%Y-%m-%d') for n in range(7)]
    _start_urls=[]
    for broadcast in broadcasts:
        for hour in range(1,24):
            for date in _dates:
                _start_urls.append('https://radiospis.pl/szukaj?stacja={broadcast}&dzien={date}&godzina={hour:02}'.format(
                    broadcast=broadcast,
                    hour=hour,
                    date=date))
    start_urls = _start_urls

    def parse(self, response):
        parser = scrapy.Selector(response)
        page = response.url.split('/')[-1].split('=')[1].split('&')[0]
        songs = parser.xpath("//div[@class='post box arc type-post status-publish format-standard hentry']")
        for song in songs:
            XPATH_SONG_NAME = ".//h2[@class='entry-title']//a/text()"
            XPATH_DATETIME = ".//p[@class='time']//text()"

            raw_song_name = song.xpath(XPATH_SONG_NAME).extract()
            raw_datetime = song.xpath(XPATH_DATETIME).extract()

            song = ''.join(raw_song_name).strip()
            sdatetime = ''.join(raw_datetime).strip()

            yield {
                'broadcast':page,
                'song_name':song,
                'datetime':sdatetime
            }

