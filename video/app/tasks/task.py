# encoding: utf-8
"""将转码和上传放入异步队列中执行"""
import os
from datetime import time

from celery import task

from app.libs.base_txy import video_txy
from app.model.video import Video, VideoSub


@task
def video_task(
        command, out_path, path_name,
        video_file_name, video_sub_id):
    # 在函数体内部引用remove_path，从而避免循环引用
    from app.utils.common import remove_path
    # print(command, out_path, path_name, video_file_name, number)

    os.system(command)  # 文件转码成功到out_path

    out_name = '.'.join([out_path, 'mp4'])  # 上传到云中的最终名称
    if not os.path.exists(out_name):
        remove_path([out_name, path_name])
        return False

    final_name = '{}_{}'.format(int(time.time()), video_file_name)
    url = video_txy.put(final_name, out_name)

    if url:
        # 如果获得了文件远程url就将其存入VideoSub数据库
        try:
            video_sub = VideoSub.objects.get(pk=video_sub_id)
            video_sub.url = url
            video_sub.save()
            return True
        except:
            return False
        finally:
            # 无论是否存入成功都要清楚两个目录里面的资源
            remove_path([out_name, path_name])
    else:
        remove_path([out_name, path_name])

