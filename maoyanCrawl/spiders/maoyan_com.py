# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from maoyanCrawl.items import MovieListItem, MovieInfoItem


# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging


class MaoyanComSpider(CrawlSpider):
    name = 'maoyan.com'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?offset=0']

    rules = (
        Rule(LinkExtractor(allow=r'\?offset=\d+'), callback='parse_movie_list', follow=True),
    )

    def parse_movie_list(self, response):
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
            ms = movie.xpath(".//div[@class='channel-detail channel-detail-orange']")
            try:
                movieScore = ms.xpath(".//i[1]/text()").extract_first() + ms.xpath(".//i[2]/text()").extract_first()
            except Exception, e:
                movieScore = ms.xpath("./text()").extract_first()

            movieListItem = MovieListItem(movieId=movieId, movieLink=movieLink, movieImgLink=movieImgLink,
                                          movieName=movieName)
            yield movieListItem
            request = scrapy.Request(url='http://maoyan.com' + movieLink, callback=self.parse_movie_detail)
            request.meta['movieId'] = movieId
            request.meta['movieScore'] = movieScore
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
        try:
            moviePTime = response.xpath(".//li[@class='ellipsis'][2]/text()").extract_first().split('/')[1]
        except Exception, e:
            moviePTime = ''
        movieRelDate = response.xpath(".//li[@class='ellipsis'][3]/text()").extract_first()

        movieBrief = response.xpath(".//div[@class='mod-content']/span/text()").extract_first()
        movieScore = response.meta['movieScore']

        movieInfoItem = MovieInfoItem(movieId=movieId, movieType=movieType, movieArea=movieArea,
                                      moviePTime=moviePTime, movieRelDate=movieRelDate, movieBoxOffice="暂无",
                                      movieBrief=movieBrief, movieScore=movieScore)
        yield movieInfoItem

# if __name__ == '__main__':
# configure_logging()
#     runner = CrawlerRunner()
#     runner.crawl(MaoyanComSpider)
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()

