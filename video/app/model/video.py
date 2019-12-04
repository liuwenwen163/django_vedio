# encoding: utf-8
"""用户视频的数据模型"""
from django.db import models
from .enums import VideoType, FromType, NationalityType


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)  # 每次更新都去修改

    class Meta:
        """联合索引一些字段，保证关键的信息不会重复"""
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return 'video name:{}'.format(self.name)


class VideoStar(models.Model):
    """演员信息的数据模型"""
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')  # 演员身份

    class Meta:
        """保证几个关键属性的唯一性"""
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return 'video_star:{}, video_name:{}'.format(self.video.name, self.video)


class VideoSub(models.Model):
    """每一集视频的数据模型"""
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{}, number:{}'.format(self.video.name, self.number)

