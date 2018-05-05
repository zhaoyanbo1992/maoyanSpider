# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
from maoyanCrawl.items import MovieListItem, MovieInfoItem


class MaoyancrawlPipeline(object):
    def __init__(self, mongo_uri, mongo_db, replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'maoyan'),
            replicaset=crawler.settings.get('REPLICASET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MovieListItem):
            self._process_movielist_item(item)
        else:
            self._process_movieinfo_item(item)
        return item

    def _process_movielist_item(self, item):
        '''
        处理电影列表数据 分析及清洗 存储
        :param item:
        :return:
        '''
        # 需要对数据进行一下清洗，类似：{movieId:10126}，提取其中的数字
        pattern = re.compile('\d+')
        match = pattern.search(item['movieId'])
        item['movieId'] = match.group() if match else item['movieId']
        self.db.movieList.insert(dict(item))

    def _process_movieinfo_item(self, item):
        '''
        处理电影详细数据 分析及清洗 存储
        :param item:
        :return:
        '''
        pattern = re.compile('\d+')

        match = pattern.search(item['movieId'])
        item['movieId'] = match.group() if match else item['movieId']

        item['movieType'] = item['movieType'].strip() if item['movieType'] else item['movieType']

        item['movieArea'] = item['movieArea'].strip() if item['movieArea'] else item['movieArea']

        match = pattern.search(item['moviePTime'])
        item['moviePTime'] = match.group() if match else item['moviePTime']

        item['movieRelDate'] = item['movieRelDate'].strip() if item['movieRelDate'] else item['movieRelDate']

        self.db.movieInfo.insert(dict(item))
