# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# from maoyanCrawl.items import MovieListItem, MovieInfoItem
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging


class MaoyanComSpider(CrawlSpider):
    name = 'maoyan.com'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?offset=0']

    rules = (
        Rule(LinkExtractor(allow=r'/films?offset=\d+'), callback='parse_movie_list', follow=True),
    )

    def parse_movie_list(self, response):
        movies = response.xpath(".//div[@class='movie-list']/dl/dd")
        print movies
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        for movie in movies:
            print movie











# if __name__ == '__main__':
#     configure_logging()
#     runner = CrawlerRunner()
#     runner.crawl(MaoyanComSpider)
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()
