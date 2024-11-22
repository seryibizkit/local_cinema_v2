import dash
from dash import dcc, html, Input, Output


import video_utils as vutils

# app = dash.Dash(__name__)
#
# # Список доступных видео
# videos = vutils.video_list()
#
# app.layout = html.Div([
#     html.H1("Список доступных видео"),
#     dcc.Dropdown(
#         id='video-dropdown',
#         options=[{'label': v, 'value': u} for v, u in videos.items()],
#         value=list(videos.values())[0]  # Устанавливаем видео по умолчанию
#     ),
#     html.Video(id='video-player', controls=True, style={'width': '60%', 'height': '60%'}),
#     html.Div(id='video-title', style={'margin-top': '20px'})
# ])
#
# @app.callback(
#     [Output('video-player', 'src'),
#      Output('video-title', 'children')],
#     Input('video-dropdown', 'value')
# )
# def update_video(selected_video):
#     return selected_video, f"Сейчас смотрите: {selected_video}"
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

app = dash.Dash(__name__)

app.layout = html.Div(style={'display': 'flex'}, children=[
    html.Div(
        html.Video(id='main-video', controls=True, style={'flex': '1'}),
        style={'flex': '1'}
    ),
    html.Div(
        html.Ul([
            html.Li(html.Button("Видео 1", id='video-1')),
            html.Li(html.Button("Видео 2", id='video-2')),
            html.Li(html.Button("Видео 3", id='video-3')),
        ]),
        style={'flex': '1'}
    )
])

@app.callback(
    Output('main-video', 'src'),
    Input('video-1', 'n_clicks'),
    Input('video-2', 'n_clicks'),
    Input('video-3', 'n_clicks')
)
def update_video(n1, n2, n3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return 'video1.mp4'  # Путь к видео по умолчанию
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'video-1':
            return 'video1.mp4'
        elif button_id == 'video-2':
            return 'video2.mp4'
        elif button_id == 'video-3':
            return 'video3.mp4'

if __name__ == '__main__':
    app.run_server(debug=True)