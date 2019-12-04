# encoding: utf-8
"""用户认证的数据模型"""
import hashlib

from django.db import models


class ClientUser(models.Model):
    """用户登录认证的视图模型"""
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=500, default='')
    gender = models.CharField(max_length=10, default='')
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'username:{}'.format(self.username)

    @classmethod
    def add(cls, username, password, avatar='', gender='',birthday=None):
        """根据用户传入的信息添加用户"""
        return cls.objects.create(
            username=username,
            password=cls.hash_password(password),
            avatar=avatar,
            gender=gender,
            birthday=birthday,
            status=True
        )

    @classmethod
    def get_user(cls, username, password):
        """尝试获取用户, 失败了就返回None"""
        try:
            user = cls.objects.get(
                username=username,
                password=cls.hash_password(password)
            )
            return user
        except:
            return None

    def update_password(self, old_password, new_password):
        """更新用户的密码"""
        hash_old_password = self.hash_password(old_password)

        if hash_old_password != self.password:
            return False
        hash_new_password = self.hash_password(new_password)

        self.password = hash_new_password
        self.save()
        return True

    def update_status(self):
        """更新用户的可用状态"""
        self.status = not self.status
        self.save()
        return True

    @staticmethod
    def hash_password(password):
        """静态方法，加密明文密码"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return hashlib.md5(password).hexdigest().upper()


