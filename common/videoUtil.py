from moviepy.editor import *
from moviepy.video.VideoClip import TextClip
from util import file_exist, JarProjectPath, get_save_path
# pip install moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple
from exp import MyException
import time


# 剪辑
def video_sub(file, start=0, end=1):
    if file_exist(file) and end > start:
        video = CompositeVideoClip([VideoFileClip(file).subclip(start, end)])
        # 写入剪辑完成的音乐
        new_video = get_save_path(origin_filepath=file)
        video.write_videofile(new_video)
        return new_video

# 合并
def video_compose(clips):
    """
    :param clips: 文件切片路径
    """
    # final_clip = concatenate_videoclips([myclip2,myclip3], method='compose') #视频合并
    # clip1 = VideoFileClip("myvideo.mp4")
    # # 结合剪辑，你甚至能够完全自动化剪辑拼接视频的操作
    # clip2 = VideoFileClip("myvideo2.mp4").subclip(50,60)
    # clip3 = VideoFileClip("myvideo3.mp4")

    if len(clips) > 1:
        final_clip = concatenate_videoclips([VideoFileClip(c) for c in clips])
        new_video = f"{JarProjectPath.project_root_path()}/files/compose_{str(round(time.time() * 1000))}.mp4"
        final_clip.write_videofile(new_video)
        return new_video
    else: 
        raise MyException('必须..至少2片段')

# 视频转GIF
def video_to_gif(file, subclip=False, start=0, end=1, resize=(488, 225), fps=30):
    """
    视频转GIF
    """
    if file_exist(file):
        if subclip:
            # .subclip(t_start=1, t_end=2) 指定长度
            clip = (VideoFileClip(file).subclip(
                t_start=start, t_end=end).resize(resize))
        else:
            # .resize((488, 225)) 指定分辨率 或百分比。
            clip = (VideoFileClip(file).resize(resize))

            # fps=15 指定帧数
        # new_gif = f"{JarProjectPath.project_root_path()}/files/{os.path.splitext(file)[0]}_{str(round(time.time() * 1000))}.gif"
        new_gif = f"{os.path.splitext(file)[0]}_{str(round(time.time() * 1000))}.gif"
        clip.write_gif(new_gif, fps=fps)
        return new_gif

# 视频添加水印，图片
def video_img_mask(file, mask=r'static/logo.png'):
    # 视频位置
    if file_exist(file) and file_exist(mask):
        video = VideoFileClip(file)

        # 准备log图片
        logo = (ImageClip(mask)
                .set_duration(video.duration)  # 水印持续时间
                .resize(height=100)  # 水印的高度，会等比缩放
                .margin(right=8, top=8, opacity=1)  # 水印边距和透明度
                .set_pos(("left", "top")))  # 水印的位置

        final = CompositeVideoClip([video, logo])
        # mp4文件默认用libx264编码， 比特率单位bps , audio_codec="aac",
        new_video = f"{os.path.splitext(file)[0]}_{str(round(time.time() * 1000))}.mp4"
        final.write_videofile(new_video, codec="libx264", bitrate="10000000")
        return new_video

# 文字水印 需安装 IMAGEMAGICK，不使用。文字转成图片 使用video_img_mask
def video_text_mask(file, text='hello world !'):
    # 视频位置
    if file_exist(file):
        video = VideoFileClip(file)
        # 制作文字，指定文字大小和颜色
        # 随着时间移动
        txt_clip = (TextClip(text).set_position(lambda t: (
            150*t, 50*t)).set_duration(video.duration))  # 水印持续时间

        result = CompositeVideoClip([video, txt_clip])  # 在视频上覆盖文本

        new_video = f"{JarProjectPath.project_root_path()}/files/movie4.mp4"
        result.write_videofile(new_video, fps=15)  # fps:视频文件中每秒的帧数
        return new_video

if __name__ == "__main__":
    path = r'static/dcf.mp4'
    path6 = 'C:/Users/dyjx/Desktop/py/images/1629353489174/sf_3.png'
    # print(os.path.splitext(path6))
    # print(JarProjectPath.project_root_path())
    # print(file_exist(r'static/logo.png'))
    
    # video_img_mask(r'static/dcf.mp4')

    # video_sub(r'files/doum.mp4', 1, 2)

    video_to_gif(r'files/compose_1633314036309.mp4')

    # video_img_mask(r'files/dcf_1633238188930.mp4')

    # video_compose([r'files/doum_1.mp4', r'files/doum_1.mp4', r'files/doum_1.mp4', r'files/doum_1.mp4'])
    # files = [r'files/dcf_1633238188930.mp4', r'files/dcf_1633238188930_1633238450194.mp4']
    # print([VideoFileClip(c) for c in files])
