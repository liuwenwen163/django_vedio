# encoding: utf-8

import functools

from django.shortcuts import redirect
from django.urls import reverse


def dashboard_auth(func):
    """定义一个装饰器，验证用户登录情况"""

    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        """
        这个装饰器是加在面向对象的get里面的
        所以传过来的参数一定有self和request
        *args和**kwargs 用来接收不确定的参数
        """
        user = request.user

        if not user.is_authenticated or not user.is_superuser:
            """验证不通过，移交到登录页面，并且在登录成功后，可以跳转回来"""
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))

        # 验证通过就让其取执行函数, func也就是传入的get函数
        return func(self, request, *args, **kwargs)

    return wrapper

