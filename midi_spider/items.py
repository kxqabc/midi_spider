#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MidiSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MidiItem(scrapy.Item):
    file_urls = scrapy.Field()
    file = scrapy.Field()
    file_name = scrapy.Field()
    artists = scrapy.Field()
    category = scrapy.Field()
    genre = scrapy.Field()