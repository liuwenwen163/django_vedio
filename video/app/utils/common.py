# encoding: utf-8
"""作为一个通用文件，起到一些验证功能"""
import os
import time
import shutil

from django.conf import settings
from app.libs.base_txy import video_txy
from app.model.video import VideoSub, Video


def check_and_get_video_type(type_obj, type_value, message):
    """验证用户传入的视频类型，国籍，来源是否符合我们定义的枚举类型"""
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}

    return {'code': 0, 'msg': 'success'}


def remove_path(paths):
    # 无论失败或者成功杀出资源
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


# 单独做一个函数，用作处理自制视频的上传
def handle_video(video_file, video_id, number):
    # 利用settings文件中的BASE_DIR文件目录的根路径，拼凑出我们要用的项目内部两个目录路径
    in_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_input')
    out_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_output')

    # 为了防止文件名重名，使用时间戳来命名文件，并且根据上面的目录拼凑出文件的绝对路径
    name = '{}_{}'.format(int(time.time()), video_file.name)
    path_name = '/'.join([in_path, name])

    # 上传后的文件是存在temp目录中的，将其移入我们的in_path
    temp_path = video_file.temporary_file_path()  # 这个目录在c盘中的一个temp目录中
    shutil.copyfile(temp_path, path_name)

    # outpath文件的绝对路径名
    out_name = '{}_{}'.format(int(time.time()), video_file.name.split('.')[0])
    out_path = '/'.join([out_path, out_name])

    # 使用ffmpeg将转码后的文件存入out_path
    command = 'ffmpeg -i {} -c copy {}.mp4'.format(path_name, out_path)
    os.system(command)  # 文件转码成功到out_path

    out_name = '.'.join([out_path, 'mp4'])  # 上传到云中的最终名称
    if not os.path.exists(out_name):
        remove_path([out_name, path_name])
        return False

    url = video_txy.put(video_file.name, out_name)
    if url:
        # 如果获得了文件远程url就将其存入VideoSub数据库
        video = Video.objects.get(pk=video_id)
        try:
            VideoSub.objects.create(
                video=video,
                url=url,
                number=number,
            )
            return True
        except:
            return False
        finally:
            # 无论是否存入成功都要清楚两个目录里面的资源
            remove_path([out_name, path_name])
    else:
        remove_path([out_name, path_name])
        return False


