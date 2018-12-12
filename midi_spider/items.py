#!/usr/bin/python
# -*- coding: UTF-8 -*-

import scrapy


class MidiItem(scrapy.Item):
    file_urls = scrapy.Field()
    file = scrapy.Field()
    song_name = scrapy.Field()
    file_name = scrapy.Field()
    artists = scrapy.Field()
    category = scrapy.Field()
    genre = scrapy.Field()