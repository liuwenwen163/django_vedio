# encoding: utf-8
from django.views.generic import View
from django.shortcuts import redirect, reverse, get_object_or_404
from app.libs.base_render import render_to_response
from app.model.comment import Comment
from app.model.enums import FromType
from app.model.video import Video
from app.utils.permission import client_auth


class ExVideo(View):
    TEMPLATE = 'client/video/video.html'

    def get(self, request):
        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data = {'videos': videos}

        return render_to_response(request, self.TEMPLATE, data=data)


class CusVideo(View):
    TEMPLATE = 'client/video/video.html'

    def get(self, request):
        videos = Video.objects.filter(from_to=FromType.custom.value)
        data = {'videos': videos}

        return render_to_response(request, self.TEMPLATE, data=data)


class VideoSub(View):
    TEMPLATE = 'client/video/video_sub.html'

    def get(self, request, video_id):
        # 拿到模板中要用的user对象和video对象
        video = get_object_or_404(Video, pk=video_id)
        user = client_auth(request)

        comments = Comment.objects.filter(video=video, status=True)

        data = {'user': user, 'video': video, 'comments': comments}
        print(user, data)
        return render_to_response(request, self.TEMPLATE, data=data)

