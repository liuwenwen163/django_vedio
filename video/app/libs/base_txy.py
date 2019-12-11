# encoding: utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

from django.conf import settings


class TXYun(object):
    def __init__(self, base_url):
        # 对象存储的初始化工作
        self.base_url = base_url
        self.bucket = settings.BUCKET
        config = CosConfig(
            Region=settings.REGION,
            SecretId=settings.TXY_ID,
            SecretKey=settings.TXY_KEY,
            Token=settings.TOKEN
        )
        self.client = CosS3Client(config)  # 实例化的上传对象


    def put(self, name, path):
        """
        上传文件的put方法
        :param name: 文件名称
        :param path: 路径
        """
        response = self.client.put_object_from_local_file(
            # Bucket为要上传的空间，由bucketname-appid组成
            Bucket=self.bucket,
            LocalFilePath=path,
            Key=name,  # 上传后保存的文件名
        )
        # print(response['ETag'])
        if response['ETag']:
            remote_url = self.base_url + name
            return remote_url

video_txy = TXYun(base_url=settings.TXY_URL)
