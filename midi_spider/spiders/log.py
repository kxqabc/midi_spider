#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging


logger = logging.getLogger("midi_spider")
logger.setLevel(level = logging.INFO)

handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)

fmt_str = '%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s'
formatter = logging.Formatter(fmt=fmt_str, datefmt='%d %b %H:%M:%S')

handler.setFormatter(formatter)
logger.addHandler(handler)

LOG_INFO = logger.info
LOG_DEBUG = logger.debug
LOG_WARM = logger.warning
LOG_ERROR = logger.error