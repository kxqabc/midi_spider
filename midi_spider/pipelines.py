#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf8')

import scrapy
from scrapy.pipelines.files import FilesPipeline

from .settings import FILES_STORE
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

STORE_PATH_PREFIX = FILES_STORE.split(os.sep, 1)[1]

class MidiSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MidiPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_urls in item['file_urls']:
            yield scrapy.Request(file_urls, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_name = item['file_name']
        category = item['category']
        return "/%s/%s.mid" % (category, file_name)


class JsonPipeline(object):

    def process_item(self, item, spider):
        # base_path = os.path.dirname(os.path.abspath('.'))
        # file_name = base_path + '/' + str(item['category']) + '/' + str(item['file_name']) + '.json'
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_name = item['file_name'] + '.json'
        # file_path = str(base_path) + '/midi/' + file_name
        file_path = os.sep.join((str(base_path), STORE_PATH_PREFIX, item['category'], 'json'))
        file_name = os.sep.join((file_path, file_name))
        if not os.path.exists(file_path):
            os.makedirs(file_path)      # 不使用os.mkdir(path), 因为不能递归创建目录
        with open(file_name, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)
        return item