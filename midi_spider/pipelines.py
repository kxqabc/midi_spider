# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MidiSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MidiPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        print('-----')
        for file_urls in item['file_urls']:
            yield scrapy.Request(file_urls, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_name = item['file_name']
        print "file_name: %s" % file_name
        return "/json/%s.mid" % file_name

