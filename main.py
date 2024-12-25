import os
import random
import dash
from dash import dcc, html, Input, Output
import dash_player as dp
import video_utils as vu

# Инициализация приложения
app = dash.Dash(__name__)

# Глобальная переменная для хранения текущей папки
current_path = '/'
home_folder = 'static/video'

videos_cur_time = vu.get_dict_from_file()

# Функция для получения фильмов и папок
def get_movies_and_folders(path):
    if path == '/':
        movie_path='static/video' + path
    else:
        movie_path='static/video/' + path
    movies = sorted([f for f in os.listdir(movie_path) if f.endswith(('.mp4', '.webm', '.avi', '.mkv'))])
    folders = sorted([d for d in os.listdir(movie_path) if os.path.isdir(os.path.join(movie_path, d))])
    return movies, folders

def get_bottom_image(img_path):
    images = [img for img in os.listdir(img_path)]
    random_image = random.choice(images)
    return str(os.path.join(img_path,random_image))

# Верстка приложения 'assets/compressed/NAEDINE_11.jpg'
app.layout = html.Div([
    html.H1("Добро пожаловать в онлайн-кинотеатр семейства Быстровых"),
    html.Div(id='folder-links', children=[], style={'text-align': 'center', 'margin-bottom': '20px', 'border-bottom': '1px solid #dedada'}),
    html.Div([
    dp.DashPlayer(id='video-player', url='', controls=True),
    dcc.Dropdown(id='movie-dropdown', options=[], style={'width': '55%', 'margin-left': '160px'}),
    html.Img(id='bottom-image',src='', height='auto', width='35%', style={'margin-left': '10px'})
    ],style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center','width': '100%'}),
    dcc.Location(id='url', refresh=False),  # Для обработки URL
    dcc.Interval(id="interval", interval=3000, n_intervals=0)   # Опрос страницы каждые три секундны для сохранения текущего состояния
    ],className="app-body")


# Служебный callback для обновления списка папок и фильмов
@app.callback(
    [Output('movie-dropdown', 'options'),
     Output('folder-links', 'children'),
     Output('bottom-image', 'src')],
    [Input('url', 'pathname')]
)
def update_movies_and_folders(pathname):
    global current_path
    current_path = pathname

    movies, folders = get_movies_and_folders(current_path)

    movie_options = [{'label': html.Span([html.Span(movie, style={'color': '#1a1a1a'})],style={'align-items': 'center', 'justify-content': 'center'}), 'value': movie} for movie in movies]
    folder_links = [html.A(folder, href=f'/{folder}', style={'color': '#ffffff','text-decoration': 'none', 'margin': '0 15px'}) for folder in folders]
    if current_path != '/':
        folder_links.append(html.A("Главная страница",href='/', style={'color': '#ffffff','text-decoration': 'none', 'margin': '0 15px'}))
    bottom_img = get_bottom_image('assets/compressed/')
    return movie_options, folder_links, bottom_img


# Обновление плеера при выборе фильма
@app.callback(
    Output('video-player', 'url'),
    Output('video-player', 'seekTo'),
    Input('movie-dropdown', 'value')
)
def display_video(movie):
    if movie:
        if current_path == '/':
            source_file = os.path.join(home_folder, movie)
        else:
            source_file = os.path.join(home_folder, current_path.strip("/"), movie)
        if videos_cur_time.get(source_file) is None:
            cur_time = 0
        else:
            cur_time = int(videos_cur_time.get(source_file))
        return str(source_file), cur_time
    return "Выберите фильм", 0

@app.callback(
    Input('video-player', 'url'),
    Input('video-player', 'currentTime'),
    Input('interval', 'n_intervals')
)
def save_current_time(src_movie, current_time, n):
    videos_cur_time.__setitem__(src_movie, current_time)
    vu.write_json_file(videos_cur_time)


# Запуск сервера
if __name__ == '__main__':
    app.run_server(host='192.168.0.110', port=7777, debug=True)