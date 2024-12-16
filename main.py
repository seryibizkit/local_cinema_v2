import os
import dash
from dash import dcc, html, Input, Output

# Инициализация приложения
app = dash.Dash(__name__)

# Глобальная переменная для хранения текущей папки
current_path = '/'
home_folder = 'static/video'


# Функция для получения фильмов и папок
def get_movies_and_folders(path):
    print('path: ' + path)
    if path == '/':
        movie_path='static/video' + path
    else:
        movie_path='static/video/' + path
    movies = [f for f in os.listdir(movie_path) if f.endswith(('.mp4', '.webm', '.avi', '.mkv'))]
    folders = [d for d in os.listdir(movie_path) if os.path.isdir(os.path.join(movie_path, d))]
    return movies, folders


# Верстка приложения
app.layout = html.Div([
    dcc.Dropdown(id='movie-dropdown', options=[], style={'width': '50%'}),
    html.Video(id='video-player', src='', controls=True, style={'height': '50%','width': '50%'}),
    html.Div(id='folder-links', children=[]),
    dcc.Location(id='url', refresh=False)  # Для обработки URL
    ])


# Служебный callback для обновления списка папок и фильмов
@app.callback(
    [Output('movie-dropdown', 'options'), Output('folder-links', 'children')],
    [Input('url', 'pathname')]
)
def update_movies_and_folders(pathname):
    global current_path
    current_path = pathname

    movies, folders = get_movies_and_folders(current_path)
    movie_options = [{'label': movie, 'value': movie} for movie in movies]
    folder_links = [html.A(folder, href=f'/{folder}', style={'margin-right': '10px'}) for folder in folders]
    if current_path != '/':
        folder_links.append(html.A("Главная страница",href='/', style={'margin-right': '10px'}))

    return movie_options, folder_links


# Обновление плеера при выборе фильма
@app.callback(
    Output('video-player', 'src'),
    Input('movie-dropdown', 'value')
)
def display_video(movie):
    if movie:
        if current_path == '/':
            source_file = os.path.join(home_folder, movie)
        else:
            source_file = os.path.join(home_folder, current_path.strip("/"), movie)
        print('movie: ' + source_file)
        return str(source_file)
    return "Выберите фильм"


# Запуск сервера
if __name__ == '__main__':
    app.run_server(host='192.168.0.110', port=7777, debug=True)