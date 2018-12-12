#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hashlib

import scrapy

from ..items import MidiItem
from log import LOG_INFO, LOG_ERROR


class MidiSpider(scrapy.Spider):
    name = "midi_spider"
    allowed_domains = ["freemidi.org"]
    # start_urls = ["https://freemidi.org/songtitle-%s-0" % e for e in ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    #  'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]
    start_urls = ["https://freemidi.org/songtitle-0-0"]

    def parse(self, response):
        main_content = response.xpath("//body/div[@id='container']/div[@id='mainContent']")
        catalog = str(main_content.xpath("./div[@class='main-content-header-div']/text()").extract_first()).strip()
        catalog = catalog[-1]
        page_selector = main_content.xpath("./div[@class='header-nav-pages-container']")
        current_page = int(page_selector.xpath("./span[@class='current']/text()").extract_first()) - 1
        # print "current page: %s" % str(current_page)
        last_page = int(page_selector.xpath("./a[last()]/text()").extract_first())
        # print "last page: %s" % str(last_page)

        print "response url: %s" % str(response.url)
        song_selectors = main_content.xpath("./div[@class='song-list-container']")
        print "len of songs: %d" % len(song_selectors)
        for song_sel in song_selectors:
            href = song_sel.xpath("./div[@class='row-title']/a/@href").extract_first()
            song_url = response.urljoin(href)
            print "song url: %s" % str(song_url)
            yield scrapy.Request(song_url, callback=self.parse_song, meta={'catalog': catalog})

        next_page = current_page + 1
        if next_page <= last_page:
            splits = response.url.split('-')[:-1]
            splits.append(str(next_page))
            next_page_url = '-'.join((splits))
            # print "next page url: %s" % str(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_song(self, response):
        category = response.meta['catalog']
        content = response.xpath("//body/"
                                  "div[@id='container']/"
                                  "div[@id='mainContent']/"
                                  "div[@class='container-fluid']/"
                                  "div[@class='row']/"
                                  "div[1]")

        midi_download_sel = content.xpath("./div[@class='container-fluid']/a[@id='downloadmidi']")
        href = midi_download_sel.xpath("./@href").extract_first()
        url = response.urljoin(href)

        song_info_sel = content.xpath("./div[1]/ol[@class='breadcrumb']")
        midi_item  = MidiItem()
        genre_sel = content.xpath("./ol[1]")
        midi_item['genre'] = []
        if genre_sel.xpath("./li[1]/text()").extract_first() == 'genre':
            for genre in genre_sel.xpath("./li[position()>1]"):
                midi_item['genre'].append(genre.xpath("./a/text()").extract_first())
        else:
            midi_item['genre'].append("none-type")
        
        midi_item['category'] = song_info_sel.xpath("./li[1]/a/span/text()").extract_first()
        if midi_item['category'] is None:
            midi_item['category'] = "none-category"
        elif midi_item['category'] == 'artists':
            midi_item['category'] = category
        midi_item['file_name'] = song_info_sel.xpath("./li[last()]/a/span/text()").extract_first()
        midi_item['artists'] = song_info_sel.xpath("./li[2]/a/span/text()").extract_first()

        # print "song info: %s" % (midi_item['category'] + '_' + midi_item['file_name'])
        midi_item['file_urls'] = [url]
        return midi_item
    
    def set_midi_item(self, song_info_sel, genre_sel):
        if not song_info_sel or not genre_sel:
            return None
        midi_item  = MidiItem()




    def add_filename_with_md5(self, midi_item):
        md5 = hashlib.md5()
        midi_info = '|'.join((midi_item['song_name'], midi_item['artists'], midi_item['genre'], midi_item['file_urls'][0]))
        md5.update(midi_info)
        md5_str = md5.hexdigest()
        midi_item['filename'] = "-".join((midi_item['song_name'], md5_str))

