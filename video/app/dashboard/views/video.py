# encoding: utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):

        return render_to_response(request, self.TEMPLATE)

