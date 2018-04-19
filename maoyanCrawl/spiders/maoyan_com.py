# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# from maoyanCrawl.items import MovieListItem, MovieInfoItem
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging


class MaoyanComSpider(scrapy.Spider):
    name = 'maoyan.com'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?offset=0']

    # rules = (
    #     Rule(LinkExtractor(allow=r'/films?offset=\d+'), callback='parse_movie_list', follow=True),
    # )

    # def parse_movie_list(self, response):
    #     movies = response.xpath(".//div[@class='movie-list']/dl/dd")
    #     print movies
    #     # from scrapy.shell import inspect_response
    #     # inspect_response(response, self)
    #
    #     for movie in movies:
    #         print movie

    def parse(self, response):
        '''
        解析列表
        :param response:
        :return:
        '''
        movies = response.xpath(".//dd")

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for movie in movies:
            movieId = movie.xpath("./div[@class='movie-item']/a/@data-val").extract_first()
            movieLink = movie.xpath("./div[@class='movie-item']/a/@href").extract_first()
            movieImgLink = movie.xpath("./div[@class='movie-item']/a/div/img[2]/@data-src").extract_first()
            movieName = movie.xpath("./div[position()=2]/a/text()").extract_first()
            print movieImgLink

# if __name__ == '__main__':
#     configure_logging()
#     runner = CrawlerRunner()
#     runner.crawl(MaoyanComSpider)
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()
