import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

data = pd.read_hdf('./Norm_games.h5')

# инициализация Dash
app = dash.Dash()

# переменные с жанрами и рейтингами для фильтрации
available_genre = data['Genre'].unique()
available_rating = data['Rating'].unique()

# определение внешнего вида приложения dash
app.layout = html.Div([
        html.Div([
            html.H1("Состояние игровой индустрии"),

            html.P(
                "Анализ игровой индустрии с 2000 по 2016 год."
                " Используйте фильтры, чтобы увидеть результат."
            )
        ], style = {
            'backgroundColor': 'rgb(230, 230, 250)',
            'padding': '10px 5px'
        }),

        # фильтр по жанрам
        html.Div([
            html.Div([
                html.Label('Жанры игр'),
                dcc.Dropdown(
                    id = 'crossfilter-genre',
                    options = [{'label': i, 'value': i} for i in available_genre],
                    # значения жанров по умолчанию
                    value = ['Sports', 'Strategy'],
                    # множественный выбор
                    multi = True 
                )
            ],
            style = {'width': '49%', 'display': 'inline-block'}),

            # фильтр по рейтингам
            html.Div([
                html.Label('Рейтинги игр'),
                dcc.Dropdown(
                    id = 'crossfilter-rating',
                    options = [{'label': i, 'value': i} for i in available_rating],
                    # значения рейтингов по умолчанию
                    value = ['T', 'E'],
                    multi = True 
                )
            ],
            style = {'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        # заготовка для интерактивного текста - результата фильтрации
        html.Div(
            id = 'textarea-output',
            style = {'width': '100%', 'float': 'right', 'display': 'inline-block'}
        ), 

        # гистограмма
        html.Div(
            dcc.Graph(id = 'histogram'),
            style = {'width': '49%', 'display': 'inline-block'}
        ), 
        
        # диаграмма рассеяния (scatter plot)
        html.Div(
            dcc.Graph(id = 'scatter-plot'),
            style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ), 

        # фильтр по годам
        html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = data['Year_of_Release'].min(),
                max = data['Year_of_Release'].max(),
                # значение по умолчанию
                value = 2008,
                step = None,
                # какие берем значения
                marks = {str(year): 
                    str(year) for year in data['Year_of_Release'].unique()}
                ), 
            style = {'width': '49%', 'padding': '0px 20px 20px 20px'}
        )
 ])

# обратный вызов результата фильтрации
@app.callback(
    Output('textarea-output', 'children'), 
    [Input('crossfilter-genre', 'value'),
    Input('crossfilter-rating', 'value'),
    Input('crossfilter-year', 'value')])
def update_textarea(genre, rating, year):
    filtered_data = data[(data['Year_of_Release'] <= year) & 
        (data['Genre'].isin(genre)) & 
        (data['Rating'].isin(rating))]
    # результат фильтрации
    games_count = len(filtered_data.index)
    return 'Результат фильтрации: {}'.format(games_count)


# обратный вызов histogram
@app.callback(
    Output('histogram', 'figure'), 
    [Input('crossfilter-genre', 'value'),
    Input('crossfilter-rating', 'value'),
    Input('crossfilter-year', 'value')])
def update_stacked_area(genre, rating, year):
    filtered_data = data[(data['Year_of_Release'] <= year) & 
        (data['Genre'].isin(genre)) & 
        (data['Rating'].isin(rating))]
    # задаем график
    figure = px.histogram(
        filtered_data, 
        x = "Year_of_Release",
        color = "Rating",
        labels = {
             "Year_of_Release": "Год релиза игр",
             "Rating": "Рейтинг"
         },
         title = "Гистограмма рейтингов игр по годам"
    )
    figure.update_layout(yaxis_title = "Кол-во")
    return figure

# обратный вызов scatter plot
@app.callback(
    Output('scatter-plot', 'figure'), 
    [Input('crossfilter-genre', 'value'),
    Input('crossfilter-rating', 'value'),
    Input('crossfilter-year', 'value')])
def update_scatter(genre, rating, year):
    filtered_data = data[(data['Year_of_Release'] <= year) & 
        (data['Genre'].isin(genre)) & 
        (data['Rating'].isin(rating))]
    # задаем график
    figure = px.scatter(
         filtered_data, 
         x = "User_Score", 
         y = "Critic_Score", 
         color = "Genre",
         labels = {
             "User_Score": "Оценка пользователей",
             "Critic_Score": "Оценка критиков",
             "Genre": "Жанр"
         },
         title = "Зависимость оценок от жанров"
    )
    return figure

if __name__ == '__main__':
    app.run_server()