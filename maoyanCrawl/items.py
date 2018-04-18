# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieListItem(scrapy.Item):
    movieId = scrapy.Field()
    movieLink = scrapy.Field()
    movieImgLink = scrapy.Field()
    movieName = scrapy.Field()


class MovieInfoItem(scrapy.Item):
    movieType = scrapy.Item()
    movieScore = scrapy.Field()
    movieArea = scrapy.Field()
    moviePTime = scrapy.Field()
    movieRelDate = scrapy.Field()
    movieBoxOffice = scrapy.Field()
    movieBrief = scrapy.Field()
