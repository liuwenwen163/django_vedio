# encoding: utf-8
"""统一存放数据模型中用到的枚举类型"""
from enum import Enum


class VideoType(Enum):
    """视频"""
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    music = 'music'
    other = 'other'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '动漫'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.music.label = '曲艺'
VideoType.other.label = '其他'


class FromType(Enum):
    """视频来源的枚举类型"""
    youku = 'youku'
    aiqiyi = 'aiqiyi'
    tengxun = 'tengxun'
    custom = 'custom'


FromType.youku.label = '优酷'
FromType.aiqiyi.label = '爱奇艺'
FromType.tengxun.label = '腾讯'
FromType.custom.label = '自制'


class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'


NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国'
NationalityType.other.label = '其他'


class IdentityType(Enum):
    to_star = 'to_star'
    supporting_rule = 'supporting_rule'
    director = 'director'


IdentityType.to_star.label = '主演'
IdentityType.supporting_rule.label = '配角'
IdentityType.director.label = '导演'

