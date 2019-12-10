# encoding: utf-8

from django.urls import path
from .views.base import Index
from .views.auth import Login, AdminManager, Logout, UpdateAdminStatus
from .views.video import (ExternalVideo, VideoSubView,
                          VideoStarView, StarDelete, SubDelete, VideoUpdate,
                          VideoUpdateStatus)

"""
这里的路由都是注册到主路由上的，所以开头都是：localhost:8001/dashboard/
"""
urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='dashboard_login'),
    path('logout', Logout.as_view(), name='logout'),
    path('admin/manager', AdminManager.as_view(), name='admin_manager'),
    path('admin/manager/update/status',
         UpdateAdminStatus.as_view(), name='admin_update_status'),
    path('video/external', ExternalVideo.as_view(), name='external_video'),
    path('video/videosub/<int:video_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/star', VideoStarView.as_view(), name='video_star'),
    path('/video/star/delete/<int:star_id>/<int:video_id>',
         StarDelete.as_view(), name='star_delete'),
    path('video/sub/delete/<int:videosub_id>/<int:video_id>',
         SubDelete.as_view(), name='sub_delete'),
    path('video/update/<int:video_id>', VideoUpdate.as_view(),
         name='video_update'),
    path('video/update/status/<int:video_id>', VideoUpdateStatus.as_view(),
         name='video_update_status')
]

