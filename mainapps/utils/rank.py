from utils import redis_cache


from house.models import *

# 加入日浏览量
def add_day_rank(house_id):
    flag = redis_cache.exists('dayrank')


    if not flag:  # 新的一天开始的时候
        redis_cache.expire('dayrank',24*60*60)
    redis_cache.zincrby('dayrank', 1, house_id)


# 获取日浏览量的所有排行id
def get_day_rank_ids():
    rank_ids = redis_cache.zrevrange('dayrank',start=0,end=100,withscores=True)
    return rank_ids