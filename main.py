import video_utils as vutils
import os
import dash
from dash import html, dcc, Input, Output
import dash_player as dp



videos = vutils.video_list("")
app = dash.Dash(__name__)
app.layout = html.Div(style={'display': 'flex'}, children=[
        html.Div(children=[
            dp.DashPlayer(id='main-video', controls=True, style={'flex': '1'}, width='100%', height='auto'),
            ],
            style={'flex': '1'}
        ),
        html.Div(
            dcc.Dropdown(
                     id='video-dropdown',
                     options=[{'label': v, 'value': u} for v, u in videos.items()],
                     value=list(videos.values())[0],  # Устанавливаем видео по умолчанию
                 ),
            style={'flex': '1'}
        )
    ])

@app.callback(
    Output('main-video', 'url'),
    Input('video-dropdown', 'value')
)
def update_video(selected_video):
    return selected_video

if __name__ == '__main__':
    app.run_server(debug=True)

