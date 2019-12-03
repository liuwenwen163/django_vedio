# encoding: utf-8
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class Login(View):
    """登录页面的"""
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        data = {'error': ''}

        # 去获取重定向过来的跳转目标to参数
        to = request.GET.get('to', '')
        data['to'] = to

        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)

        data = {}

        exists = User.objects.filter(username=username).exists()
        if not exists:
            data = {'error': '不存在该用户'}
            return render_to_response(request, self.TEMPLATE, data=data)

        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = "您无权登录"
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)

        # 如果有跳转参数,就按照跳转参数跳转
        to = request.GET.get('to', '')
        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


class Logout(View):
    """用户注销的视图函数逻辑"""
    def get(self, request):
        logout(request)
        return redirect(reverse('dashboard_login'))


class AdminManager(View):
    """管理员管理用户的视图函数逻辑"""
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.filter()

        # 获取url中的page参数，没有就设为1
        page = request.GET.get('page', 1)
        # 实例化分页器对象，第一个参数是对象列表，第二个参数是每页数据
        p = Paginator(users, 3)
        # 从实例化的p对象的num_pages属性拿到总页数
        total_page = p.num_pages

        if int(page) <= 1:
            page = 1

        # 通过get_page获取对应的页面，然后通过object_list拿到对应的显示数据
        current_page = p.get_page(int(page)).object_list

        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):

    def get(self, request):
        status = request.GET.get('status', 'on')

        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))

