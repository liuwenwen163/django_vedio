# encoding: utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse

from app.libs.base_render import render_to_response
from app.model.video import Video, VideoSub, VideoStar
from app.utils.permission import dashboard_auth
from app.model.enums import VideoType, FromType, NationalityType, IdentityType
from app.utils.common import check_and_get_video_type


class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):

        error = request.GET.get('error', '')
        data = {'error': error}

        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos

        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')

        if not all([name, image, video_type, from_to, nationality, info]):
            return redirect(
                '{}?error={}'.format(reverse('external_video'), '缺少必要字段')
            )

        # 调用自定义的check函数验证 video_type 是否符合枚举类型
        # VideoType本身就是一个枚举类型，所以可以传入函数进行判断
        result = check_and_get_video_type(
            VideoType, video_type, '非法视频类型'
        )
        if result.get('code') != 0:
            return redirect(
                '{}?error={}'.format(reverse('external_video'), result['msg'])
            )

        # 验证 from_to 是否符合定义的枚举类型
        result = check_and_get_video_type(
            FromType, from_to, '非法的来源'
        )
        if result.get('code') != 0:
            return redirect(
                '{}?error={}'.format(reverse('external_video'), result['msg'])
            )

        # 验证 nationality 是否符合定义的枚举类型
        result = check_and_get_video_type(
            NationalityType, nationality, '非法的国籍信息'
        )
        if result.get('code') != 0:
            return redirect(
                '{}?error={}'.format(reverse('external_video'), result['msg'])
            )

        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_to=from_to,
            nationality=nationality,
            info=info
        )

        return redirect(reverse('external_video'))


class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error', '')
        data['video'] = video
        data['error'] = error

        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        video = Video.objects.get(pk=video_id)

        url = request.POST.get('url')

        # 获取集数
        length = video.video_sub.count()

        try:
            VideoSub.objects.create(video=video, url=url, number=length + 1)
        except:
            path_format = '{}'.format(reverse('video_sub', kwargs={'video_id': video_id}))
            return redirect('{}?error={}'.format(path_format, '不可重复创建'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoStarView(View):
    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        path_format = '{}'.format(reverse('video_sub', kwargs={'video_id': video_id}))

        if not all([name, identity, video_id]):
            return redirect('{}?error={}'.format(path_format, '缺少必要字段'))

        result = check_and_get_video_type(
            IdentityType, identity, '非法的身份'
        )
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format, result['msg']))

        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(
                video=video,
                name=name,
                identity=identity
            )
        except:
            return redirect('{}?error={}'.format(path_format, '创建失败'))


        return redirect(
            reverse('video_sub', kwargs={
                'video_id': video_id,
            })
        )


class StarDelete(View):
    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()

        return redirect(
            reverse('video_sub', kwargs={
                'video_id': video_id,
            })
        )

