#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import hashlib

import scrapy

from ..items import MidiItem
from log import LOG_INFO, LOG_ERROR


DEFAULT_CATEGORY = ("tv themes", "movie themes", "video games", "seasonal", "national anthems")


class MidiSpider(scrapy.Spider):
    name = "midi_spider"
    allowed_domains = ["freemidi.org"]
    # start_urls = ["https://freemidi.org/songtitle-%s-0" % e for e in ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    #  'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']]
    start_urls = ["https://freemidi.org/songtitle-a-0"]

    def parse(self, response):
        print "response url: %s" % str(response.url)
        main_content = response.xpath("//body/div[@id='container']/div[@id='mainContent']")
        # parse catalog
        catalog = str(main_content.xpath("./div[@class='main-content-header-div']/text()").extract_first()).strip()
        catalog = catalog[-1]
        # parse current page num and last page num in this page
        page_selector = main_content.xpath("./div[@class='header-nav-pages-container']")
        current_page = int(page_selector.xpath("./span[@class='current']/text()").extract_first()) - 1
        last_page = int(page_selector.xpath("./a[last()]/text()").extract_first())
        # download midi and song's info
        song_selectors = main_content.xpath("./div[@class='song-list-container']")
        print "len of songs: %d" % len(song_selectors)
        for song_sel in song_selectors:
            href = song_sel.xpath("./div[@class='row-title']/a/@href").extract_first()
            song_url = response.urljoin(href)
            yield scrapy.Request(song_url, callback=self.parse_song, meta={'catalog': catalog})
        # go to the next page if exist
        next_page = current_page + 1
        if next_page <= last_page:
            splits = response.url.split('-')[:-1]
            splits.append(str(next_page))
            next_page_url = '-'.join((splits))
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_song(self, response):
        catalog = response.meta['catalog']
        content = response.xpath("//body/"
                                  "div[@id='container']/"
                                  "div[@id='mainContent']/"
                                  "div[@class='container-fluid']/"
                                  "div[@class='row']/"
                                  "div[1]")
        # parse download url
        download_url = self.parse_download_url(content, response)
        # parse song info selector
        song_info_sel = content.xpath("./div[1]/ol[@class='breadcrumb']")
        genre_sel = content.xpath("./ol[1]")
        # create midi item, using pipeline to keep it in json and midi files
        midi_item = self.set_midi_item(song_info_sel, genre_sel,url=download_url, catalog=catalog)
        return midi_item
    
    def parse_download_url(self, content_selector, response):
        if not content_selector:
            LOG_ERROR("download content selector is invalid, midi_url: %s" % str(response.url))
            raise ValueError
        midi_download_sel = content_selector.xpath("./div[@class='container-fluid']/a[@id='downloadmidi']")
        href = midi_download_sel.xpath("./@href").extract_first()
        download_url = response.urljoin(href)
        if not download_url:
            LOG_ERROR("download url is invalid, midi_url: %s" % str(response.url))
            raise ValueError
        return download_url
    
    def set_midi_item(self, song_info_sel, genre_sel, url="default_url", catalog="default"):
        if not song_info_sel or not genre_sel:
            LOG_ERROR("song_info_sel or genre_sel is invalid, midi_url: %s" % str(url))
            raise ValueError
        midi_item  = MidiItem()
        # parse and set midi info
        info_sels = song_info_sel.xpath("./li")
        if len(info_sels) < 2 or len(info_sels) > 3:
            LOG_ERROR("the midi has no info, midi_url: %s" % str(url))
            raise ValueError
        elif len(info_sels) == 2:    
            song_name = song_info_sel.xpath("./li[2]/a/span/text()").extract_first()
            artists = "no-artists"
        elif len(info_sels) == 3:
            song_name = song_info_sel.xpath("./li[last()]/a/span/text()").extract_first()
            artists = song_info_sel.xpath("./li[2]/a/span/text()").extract_first()
        midi_item['song_name'] = song_name
        midi_item['artists'] = artists
        midi_item['file_urls'] = [url]
        # parse and set midi genre
        midi_item['genre'] = []
        if genre_sel.xpath("./li[1]/text()").extract_first() == 'genre':
            for genre in genre_sel.xpath("./li[position()>1]"):
                midi_item['genre'].append(genre.xpath("./a/text()").extract_first())
        else:
            midi_item['genre'].append("none-type")
        # set catalog
        category = song_info_sel.xpath("./li[1]/a/span/text()").extract_first()
        if not category:
            midi_item['category'] = "default"
        elif category == 'artists':
            midi_item['category'] = catalog
        elif category in DEFAULT_CATEGORY:
            midi_item['category'] = category
        else:
            LOG_ERROR("the midi's category is invalid, midi_url: %s" % str(url))
            raise ValueError
        # set file name with md5
        self.add_filename_with_md5(midi_item)
        return midi_item

    def add_filename_with_md5(self, midi_item):
        md5 = hashlib.md5()
        curr_time = str(time.time())
        midi_info = '|'.join((midi_item['song_name'], midi_item['artists'], curr_time))
        md5.update(midi_info)
        md5_str = md5.hexdigest()
        midi_item['file_name'] = "-".join((midi_item['song_name'], md5_str))

