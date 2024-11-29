import os


def video_list(video_path = ""):
    videos_list = {}
    if video_path == "":
        video_path = 'static/video'
    for file in os.listdir(video_path):
        if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm'):
            filename = os.path.join(video_path, file)
            videos_list.__setitem__(file,filename)
    return videos_list
