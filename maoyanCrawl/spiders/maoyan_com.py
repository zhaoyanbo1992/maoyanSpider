# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from maoyanCrawl.items import MovieListItem, MovieInfoItem


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

            movieListItem = MovieListItem(movieId=movieId, movieLink=movieLink, movieImgLink=movieImgLink,
                                          movieName=movieName)
            yield movieListItem
            request = scrapy.Request(url='http://maoyan.com' + movieLink, callback=self.parse_movie_detail)
            request.meta['movieId'] = movieId
            yield request

    def parse_movie_detail(self, response):
        '''
        解析详情页面信息
        :param response:
        :return:
        '''
        movieId = response.meta['movieId']
        movieType = response.xpath(".//li[@class='ellipsis'][1]/text()").extract_first()
        movieArea = response.xpath(".//li[@class='ellipsis'][2]/text()").extract_first().split('/')[0]
        moviePTime = response.xpath(".//li[@class='ellipsis'][2]/text()").extract_first().split('/')[1]
        movieRelDate = response.xpath(".//li[@class='ellipsis'][3]/text()").extract_first()
        movieBoxOffice = response.xpath(
            ".//div[@class='movie-index-content box']/span[1]/text()").extract_first() + response.xpath(
            ".//div[@class='movie-index-content box']/span[2]/text()").extract_first()
        movieBrief = response.xpath(".//div[@class='mod-content']/span/text()").extract_first()
        movieScore = response.xpath(
            ".//div[@class='movie-index-content score normal-score']/span/text()").extract_first()

        movieInfoItem = MovieInfoItem(movieId=movieId, movieType=movieType, movieArea=movieArea,
                                      moviePTime=moviePTime, movieRelDate=movieRelDate, movieBoxOffice=movieBoxOffice,
                                      movieBrief=movieBrief, movieScore=movieScore)
        yield movieInfoItem

# if __name__ == '__main__':
# configure_logging()
#     runner = CrawlerRunner()
#     runner.crawl(MaoyanComSpider)
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()
