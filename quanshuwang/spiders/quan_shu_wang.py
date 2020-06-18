# -*- coding: utf-8 -*-
import os

import scrapy

from ..items import BookChapterItem, BookImageItem, BookInfoItem
from ..import settings


class QuanShuWangSpider(scrapy.Spider):
    name = 'quan_shu_wang'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/all/allvisit_0_0_0_0_0_0_1.html']

    def __init__(self, *args, max_page=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_CurPage = 1
        self.m_MaxPage = int(max_page)

    def _has_txt(self, dirname):
        for filename in os.listdir(dirname):
            if filename.endswith(".txt"):
                return True
        return False

    def parse(self, response):
        for book in response.xpath('//div[@class="tab-item clearfix"]/div'):
            bookname = book.xpath('./a/img/@alt').get()
            bookdir = os.path.join(settings.IMAGES_STORE, bookname)
            if self._has_txt(bookdir):
                continue
            bookurl = book.xpath('./a/@href').get()
            yield scrapy.Request(bookurl, callback=self.parse_book_info, priority=1)

        self.m_CurPage += 1
        if self.m_CurPage > self.m_MaxPage:
            return

        next_url = response.xpath('//div[@class="pagelink"]/a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(next_url, priority=0)

    def parse_book_info(self, response):
        oBookInfoItem = BookInfoItem()
        oBookImageItem = BookImageItem()
        oDetail = response.xpath('//div[@class="detail"]')[0]
        book_url = oBookInfoItem["url"] = oDetail.xpath('./a/@href').get()
        book_name = oBookImageItem["name"] = oBookInfoItem["name"] = oDetail.xpath('./a/img/@title').get()
        oBookImageItem["url"] = oDetail.xpath('./a/img/@src').get()
        oBookInfoItem["statue"] = oDetail.xpath('./div[@class="author"]/div/dl/dd/text()').get()
        oBookInfoItem["author"] = oDetail.xpath('./div[@class="author"]/div/dl[@class="bookso"]/dd/text()').get().strip()
        oBookInfoItem["save_num"] = oDetail.xpath('//a[@class="meNum"]/text()').get()
        oBookInfoItem["like_num"] = oDetail.xpath('//a[@class="meNum"]/text()')[1].extract()

        yield oBookImageItem
        yield oBookInfoItem
        yield scrapy.Request(book_url, callback=self.parse_book_chapter, priority=2, meta={"bookname": book_name})

    def parse_book_chapter(self, response):
        bookname = response.meta["bookname"]
        for chapter in response.xpath('//div[@class="clearfix dirconone"]/li'):
            chapter_url = chapter.xpath('./a/@href').get()
            chapter_name = chapter.xpath('./a/text()').get().strip()
            yield scrapy.Request(chapter_url, callback=self.parse_book_chapter_content, priority=3, meta={"bookname": bookname, "chaptername": chapter_name})

    def parse_book_chapter_content(self, response):
        item = BookChapterItem()
        chapter_id = response.url.split("/")[-1].split(".")[0]
        item["book_name"] = response.meta["bookname"]
        chapter_name = response.meta["chaptername"].strip()
        item["chapter_name"] = str(chapter_id) + "_" + chapter_name.replace("/", "")
        contents = ""
        for content in response.xpath('//div[@class="mainContenr"]/text()'):
            content = content.get().replace('    ', '').replace('<br />', '')
            contents += content
        item["content"] = contents
        yield item
