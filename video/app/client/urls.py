# encoding: utf-8
from django.urls import path

from app.client.views.auth import User, Regist, Logout
from .views.base import Index
from .views.video import ExVideo, VideoSub, CusVideo

urlpatterns = [
    path('', Index.as_view(), name='client_index'),
    path('video/ex', ExVideo.as_view(), name='client_ex_video'),
    path('video/<int:video_id>', VideoSub.as_view(), name='client_video_sub'),
    path('video/custom', CusVideo.as_view(), name='client_cus_video'),
    path('auth', User.as_view(), name='client_user'),
    path('auth/regist', Regist.as_view(), name='client_regist'),
    path('auth/logout', Logout.as_view(), name='client_logout'),
]

