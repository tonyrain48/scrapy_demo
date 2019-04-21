# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field,Item


class RestaurantItem(scrapy.Item):
    #城市信息
    city_id=Field()     #
    city_name=Field()   #
    city_prov=Field()
    total_restaurant=Field()
    total_comment=Field()

    #美食餐厅表
    rest_id=Field()         #
    rest_CH_name=Field()    #
    rest_rank=Field()       #
    comm_num=Field()        #
    rest_score=Field()      #
    food_score=Field()      #
    serve_score=Field()     #
    cost_score=Field()      #
    address=Field()     #
    phone=Field()       #
    pic_num=Field()     #
    food_type=Field()   #
    spec_food=Field()   #
    meal_time=Field()   #
    open_close=Field()

    #评论表
    comm_id=Field()         #
    meal_date=Field()       #因为有的有有的没有，暂时不爬取
    comm_date=Field()       #
    comm_name=Field()       #
    comm_score=Field()      #
    thanks_num=Field()      #有的有有的没有
    comm_content=Field()     #
    comm_title=Field()       #
    rest_reply=Field()      #有的有有的没有
    reply_content=Field()   #有的有有的没有
    rating_5=Field()    #
    rating_4=Field()    #
    rating_3=Field()    #
    rating_2=Field()    #
    rating_1=Field()    #

    '''
    暂时不做评论人表

    commentator_name=Field()
    commentator_level=Field()
    join_time=Field()
    commentator_city=Field()
    comment_recommend=Field()
    comment_shared=Field()
    city_gone=Field()
    comm_pic_num=Field()
    '''

    #附近酒店表
    nearby_hotel_id=Field()         #
    nearby_hotel_name=Field()       #
    nearby_hotel_dist=Field()       #

    #附近餐厅表
    nearby_rest_id=Field()          #
    nearby_rest_name=Field()        #
    nearby_rest_dist=Field()        #

    #附近景点表
    nearby_spot_id=Field()          #
    nearby_spot_name=Field()        #
    nearby_spot_dist=Field()        #
