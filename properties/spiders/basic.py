# -*- coding: utf-8 -*-
import scrapy
from properties.items import RestaurantItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,Join
from urllib.parse import urljoin
from scrapy import Request
from scrapy.spiders import CrawlSpider
import re

class BasicSpider(CrawlSpider):
    name = 'basic'
    start_urls = ['https://www.tripadvisor.cn/Restaurants-g294211-China.html']
    download_delay = 0.3

    def item_parse(self,response):
        l=ItemLoader(item=RestaurantItem(),response=response)

        '''
        餐厅基本信息
        '''

        #城市id
        try:
            l.add_xpath('city_id','//div[@class="global-nav-geopill"]/@data-id')
        except:
            pass

        #城市名称
        try:
            l.add_xpath('city_name','//div[@class="global-nav-geopill"]/span//text()')
        except:
            pass

        #餐厅id
        try:
            l.add_xpath('rest_id','//div[@class="blRow  "]/attribute::data-locid')
        except:
            pass

        #餐厅名
        try:
            l.add_xpath('rest_CH_name','//*[@class="ui_header h1"]/text()')
        except:
            pass

        #联系方式
        try:
            l.add_xpath('phone','//*[@class="detail  is-hidden-mobile"]/text()')
        except:
            pass

        #地址，用string()提取子标签所有文本内容
        try:
            l.add_xpath('address','string(//span[@class="detail "])')
        except:
            pass

        #餐厅排名(只提取第一个元素)
        try:
            l.add_xpath('rest_rank','(//span[@class=""])[1]/text()')
        except:
            pass

        #点评数量
        try:
            l.add_xpath('comm_num','//span[@class="reviews_header_count"]/text()',
                         MapCompose(int),re='[.0-9]+')
        except:
            pass

        #餐厅评分
        try:
            l.add_xpath('rest_score',
                         '//span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl"]/text()',
                         MapCompose(float),re='[,.0-9]+')
        except:
            pass

        #食物，服务，实惠，用attribute::class提取
        other_rank = response.xpath(
            '//span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC"]/span[starts-with(@class,"ui_bubble")]/attribute::class').extract()

        try:
            food_score=float(re.sub("\D", "", other_rank[0]))/10.0
        except:
            pass
        else:
            l.add_value('food_score',food_score)

        try:
            serve_score=float(re.sub("\D", "", other_rank[1]))/10.0
        except:
            pass
        else:
            l.add_value('serve_score',serve_score)

        try:
            cost_score =float(re.sub("\D", "", other_rank[2]))/10.0
        except:
            pass
        else:
            l.add_value('cost_score',cost_score)

        #食物种类，通过text查找，寻找兄弟节点值
        try:
            l.add_xpath('food_type',
                        '//div[contains(text(),"\u7f8e\u98df")]/following-sibling::div/text()')
        except:
            l.add_value('food_type','N/A')

        #特殊食物
        try:
            l.add_xpath('spec_food',
                        '//div[contains(text(),"\u7279\u6b8a\u996e\u98df")]/following-sibling::div/text()')
        except:
            l.add_value('spec_food','N/A')

        #餐时
        try:
            l.add_xpath('meal_time',
                        '//div[contains(text(),"\u9910\u65f6")]/following-sibling::div/text()')
        except:
            l.add_value('meal_time','N/A')

        #图片数量
        try:
            l.add_xpath('pic_num','(//*[@class="details"])[1]/text()',
                        MapCompose(int),re='[.0-9]+')
        except:
            pass

        '''
        评论信息
        '''
        #5分评价数
        try:
            l.add_xpath('rating_5',
                '(//label[text()="\u975e\u5e38\u597d"])[1]/following-sibling::span[@class="row_num  is-shown-at-tablet"]/text()',
                MapCompose(int))
        except:
            pass

        #4分评价数
        try:
            l.add_xpath('rating_4',
                '(//label[text()="\u8f83\u597d"])[1]/following-sibling::span[@class="row_num  is-shown-at-tablet"]/text()',
                MapCompose(int))
        except:
            pass

        #3分评价数
        try:
            l.add_xpath('rating_3',
                '(//label[text()="\u4e00\u822c"])[1]/following-sibling::span[@class="row_num  is-shown-at-tablet"]/text()',
                MapCompose(int))
        except:
            pass

        #2分评价数：
        try:
            l.add_xpath('rating_2',
                '(//label[text()="\u8f83\u5dee"])[1]/following-sibling::span[@class="row_num  is-shown-at-tablet"]/text()',
                MapCompose(int))
        except:
            pass

        # 1分评价数：
        try:
            l.add_xpath('rating_1',
                '(//label[text()="\u5f88\u5dee"])[1]/following-sibling::span[@class="row_num  is-shown-at-tablet"]/text()',
                MapCompose(int))
        except:
            pass

        #评论id
        try:
            l.add_xpath('comm_id','//div[@class="reviewSelector"]/attribute::data-reviewid')
        except:
            pass

        #评论人名称
        try:
            l.add_xpath('comm_name','//div[@class="info_text"]/div/text()')
        except:
            pass

        #评论标题
        try:
            l.add_xpath('comm_title','//span[@class="noQuotes"]/text()')
        except:
            pass

        #评论内容
        try:
            l.add_xpath('comm_content','//div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]//text()')
        except:
            pass

        #评论时间
        try:
            l.add_xpath('comm_date','//span[@class="ratingDate"]/attribute::title')
        except:
            pass

        #评价分数
        try:
            comm_score=response.xpath('//div[@class="rev_wrap ui_columns is-multiline "]//span[starts-with(@class,"ui_bubble_rating")]//attribute::class').extract()
            for i in range(len(comm_score)):
                comm_score[i]=float(re.sub("\D", "", comm_score[i]))/10.0
        except:
            pass
        else:
            l.add_value('comm_score',comm_score)


        '''
        附近环境信息
        '''

        #附近酒店id
        l.add_xpath('nearby_hotel_id',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[1]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-locid')

        #附近酒店名称
        l.add_xpath('nearby_hotel_name',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[1]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-name')

        #附近酒店距离
        l.add_xpath('nearby_hotel_dist',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[1]//div[@class="distance"]/text()')

        # 附近餐厅id
        l.add_xpath('nearby_rest_id',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[2]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-locid')

        # 附近餐厅名称
        l.add_xpath('nearby_rest_name',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[2]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-name')

        # 附近餐厅距离
        l.add_xpath('nearby_rest_dist',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[2]//div[@class="distance"]/text()')

        # 附近景点id
        l.add_xpath('nearby_spot_id',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[3]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-locid')

        # 附近景点名称
        l.add_xpath('nearby_spot_name',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[3]//div[@class="ui_columns is-gapless is-mobile poiEntry shownOnMap"]/attribute::data-name')

        # 附近景点距离
        l.add_xpath('nearby_spot_dist',
                    '(//div[@class="ui_columns is-multiline nearbyGrid"])[3]//div[@class="distance"]/text()')

        return l.load_item()

    def city_parse(self, response):
        next_selector=response.xpath('//*[@class="nav next rndBtn ui_button primary taLnk"][1]//@href')
        for url in next_selector.extract():
            yield Request(urljoin("https://www.tripadvisor.cn/",url),callback=self.city_parse)

        item_selector=response.xpath('//*[starts-with(@id,"eatery")]//*[@class="property_title"]/@href')
        for url in item_selector.extract():
            yield Request(urljoin("https://www.tripadvisor.cn/",url),callback=self.item_parse)

    def parse(self,response):
        next_selector=response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]//@href')
        for url in next_selector.extract():
            yield Request(urljoin("https://www.tripadvisor.cn/",url),callback=self.parse)

        city_selector=response.xpath('//div[@class="geo_name"]/a/@href')
        for url in city_selector.extract():
            yield Request(urljoin("https://www.tripadvisor.cn/",url),callback=self.city_parse)
