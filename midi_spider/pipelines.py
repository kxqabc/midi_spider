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

STORE_PATH_PREFIX = FILES_STORE.split(os.sep, 1)[1]


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
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_name = item['file_name'] + '.json'
        file_path = os.sep.join((str(base_path), STORE_PATH_PREFIX, item['category'], 'info'))
        file_name = os.sep.join((file_path, file_name))
        if not os.path.exists(file_path):
            os.makedirs(file_path)      # 不使用os.mkdir(path), 因为不能递归创建目录
        with open(file_name, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)
        return item