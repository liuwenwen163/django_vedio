# encoding: utf-8
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from app.libs.base_render import render_to_response


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        data = {'error': ''}
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {}
        # print(username, password)
        exists = User.objects.filter(username=username).exists()
        data = {'error': '不存在该用户'}
        if not exists:
            return render_to_response(request, self.TEMPLATE, data=data)

        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = "您无权登录"
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)
        return redirect(reverse('dashboard_index'))
