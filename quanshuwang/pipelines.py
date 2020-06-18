# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from . import settings
from .items import BookChapterItem, BookImageItem, BookInfoItem


class BookChapterPipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, BookChapterItem):
            return item
        book_name = item["book_name"]
        chapter_dir = os.path.join(settings.IMAGES_STORE, book_name)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
        chapter_file = os.path.join(chapter_dir, item["chapter_name"] + ".txt")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(item["content"] + "\n")
        return item


class BookInfoPipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, BookInfoItem):
            return item
        csvpath = os.path.join(settings.IMAGES_STORE, "book.csv")
        info = f"{item['name']},{item['author']},{item['statue']},{item['save_num']},{item['like_num']},{item['url']}\n"
        with open(csvpath, "a+", encoding="utf-8") as f:
            f.write(info)
        return item


class BookImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if not isinstance(item, BookImageItem):
            return
        image_url = item["url"]
        yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        name = request.meta["item"]["name"]
        image_suf = request.url.split('.')[-1]
        return f"./{name}/{name}.{image_suf}"
