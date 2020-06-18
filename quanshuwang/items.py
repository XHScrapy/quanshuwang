# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanshuwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookInfoItem(scrapy.Item):
    author = scrapy.Field()
    name = scrapy.Field()
    statue = scrapy.Field()
    url = scrapy.Field()
    save_num = scrapy.Field()   # 加入书架数量
    like_num = scrapy.Field()   # 点赞数量


class BookImageItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()


class BookChapterItem(scrapy.Item):
    book_name = scrapy.Field()
    chapter_name = scrapy.Field()
    content = scrapy.Field()
