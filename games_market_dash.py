import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

data = pd.read_hdf('./Norm_games.h5')

app = dash.Dash()

available_genre = data['Genre'].unique()
available_rating = data['Rating'].unique()


app.layout = html.Div([
        html.Div([
            html.H1("Состояние игровой индустрии"),

            html.P(
                "Анализ игровой индустрии с 2000 по 2016 год."
                " Используйте фильтры, чтобы увидеть результат."
            )
        ], style={
            'backgroundColor': 'rgb(230, 230, 250)',
            'padding': '10px 5px'
        }),

        html.Div([
            html.Div([
                html.Label('Жанры игр'),
                dcc.Dropdown(
                    id='crossfilter-genre',
                    options=[{'label': i, 'value': i} for i in available_genre],
                    value=['Sports', 'Strategy'],
                    multi=True 
                )
            ],
            style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                html.Label('Рейтинги игр'),
                dcc.Dropdown(
                    id='crossfilter-rating',
                    options=[{'label': i, 'value': i} for i in available_rating],
                    value=['T', 'E'],
                    multi=True 
                )
            ],
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        html.Div([
            dcc.Textarea(
                #id= ,
                
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}), 

        html.Div([
            dcc.Graph(
                id='stacked-area-plot' 
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}), 

        html.Div([
            dcc.Graph(
                id='scatter-plot'
            )
        ],
        style={'width': '49%', 'float': 'right', 'display': 'inline-block'}), 

        html.Div([
            dcc.Slider(
                id='crossfilter-year',
                min=data['Year_of_Release'].min(),
                max=data['Year_of_Release'].max(),
                value=2008,
                step=None,
                marks={str(year): str(year) for year in data['Year_of_Release'].unique()}
                ) 
        ], 
        style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

@app.callback(
    Output('stacked-area-plot', 'figure'), 
    [Input('crossfilter-genre', 'value'),
    Input('crossfilter-rating', 'value'),
    Input('crossfilter-year', 'value'),])
def  update_graph():

    return {
        
    }



if __name__ == '__main__':
    app.run_server()