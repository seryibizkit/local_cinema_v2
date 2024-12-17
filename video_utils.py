import os, json
from PIL import Image
from moviepy import VideoFileClip


def video_list(video_path = ""):
    videos_list = {}
    if video_path == "":
        video_path = 'static/video'
    for file in os.listdir(video_path):
        if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm'):
            filename = os.path.join(video_path, file)
            videos_list.__setitem__(file,filename)
    return videos_list

def file_thumbnail(source_path):
    # Загрузка видеофайла
    name = os.path.splitext(os.path.basename(source_path))[0]

    # Создание папки для thumbnail
    thumbnails_dir = "static/thumbnails"
    os.makedirs(thumbnails_dir, exist_ok=True)
    new_image_filepath = os.path.join(thumbnails_dir, f"{name}_thumbnail.jpg")
    if os.path.isfile(new_image_filepath ):
        return new_image_filepath
    else:
        # Создание объекта VideoFileClip
        clip = VideoFileClip(source_path)

        # Получение количества кадров в секунду
        fps = clip.reader.fps

        # Получение количества кадров в видео
        nframes = clip.reader.n_frames

        # Получение длительности видео в секундах
        duration = clip.duration

        # Создание thumbnail на определенном кадре
        frame_at_second = float(duration * 10 / 100)
        frame = clip.get_frame(frame_at_second)

        # Сохранение thumbnail в файл
        new_image = Image.fromarray(frame)
        new_image.save(new_image_filepath)
        return new_image_filepath

def get_dict_from_file(file_path="static/videos.json"):
    if not os.path.exists(file_path):
        return {}  # Возвращаем пустой словарь, если файл не существует
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, file_path="static/videos.json"):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
