import pandas as pd
import numpy as np
#from sentiment_analysis import * # Deixar fora do comentário apenas se for fazer o ETL completo
import plotly.graph_objs as go
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table
from dash.dependencies import Input, Output
from app import *
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud
import io
from PIL import Image
import openai
from keys import openai_Key




merged_df = pd.read_csv('/home/renan/Documents/Projects/Project_A3/Resources/merged.csv')

config_graph={"displayModeBar": False, "showTips": False}
app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
app.layout = dbc.Container(children=[
    # ROW 1
    dbc.Row(dbc.Col(html.H1(children="Análise de dados de livros"), width=12)),
    # ROW 2
    dbc.Row([
        dbc.Col([
            html.H5('Selecione o autor'),
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        id='authors',
                        options=[{'label': i, 'value': i} for i in merged_df['authors'].unique()],
                        multi=True
                    )
                ])
            ])
        ]),
        dbc.Col([
            html.H5('Selecione o título'),
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        id='title',
                        multi=True
                    )
                ])
            ])
        ]),
        dbc.Col([
            html.H5('Selecione a categoria'),
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                        id='categories',
                        multi=True
                    )
                ])
            ])
        ])
    ]),
    # ROW 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='positive_negative',className='graph', config=config_graph) 
                ])
            ])
        ],sm=12,md=6,lg=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', className='graph', config=config_graph) 
                ])
            ])
        ],sm=12,md=6,lg=8),

    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     html.Div(id='text_result')
                ])
            ])
        ],sm=12,md=12,lg=12),
    ])


])

@app.callback(
    Output('title', 'options'),
    Input('authors', 'value')
)
def update_title_dropdown(selected_authors):
    if selected_authors:
        filtered_df = merged_df[merged_df['authors'].isin(selected_authors)]
    else:
        filtered_df = merged_df
    return [{'label': i, 'value': i} for i in filtered_df['Title'].unique()]

@app.callback(
    Output('categories', 'options'),
    Input('authors', 'value')
)
def update_category_dropdown(selected_authors):
    if selected_authors:
        filtered_df = merged_df[merged_df['authors'].isin(selected_authors)]
    else:
        filtered_df = merged_df
    return [{'label': i, 'value': i} for i in filtered_df['categories'].unique()]


# Gráfico 1 (Pizza)
@app.callback(
    Output('positive_negative', 'figure'),
    Input('authors', 'value'),
    Input('title', 'value'),
    Input('categories', 'value')
)
def positive_negative(authors, title, categories):
    fill_df = merged_df.query("authors.isin(@authors) & Title.isin(@title) & categories.isin(@categories)")
    count_df = fill_df['sentiment_label_summary'].value_counts().reset_index()
    count_df.columns = ['sentiment_label_summary', 'count']

    fig = px.pie(count_df, values='count', names='sentiment_label_summary')

    return fig

# Grafico de Wordcloud
@app.callback(
    Output('wordcloud', 'figure'),
    Input('authors', 'value'),
    Input('title', 'value'),
    Input('categories', 'value')
)

def wordcloud(authors, title, categories):
    fill_df = merged_df.query("authors.isin(@authors) & Title.isin(@title) & categories.isin(@categories)")
    all_text = ' '.join(fill_df['text'])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    image_stream = io.BytesIO()
    wordcloud.to_image().save(image_stream, format='PNG')
    image_stream.seek(0)

    image_stream = io.BytesIO()
    wordcloud.to_image().save(image_stream, format='PNG')
    image_stream.seek(0)

    # Carregar a imagem como uma matriz numpy
    image_pil = Image.open(image_stream)
    image_array = np.array(image_pil)

    # Criar figura Plotly
    fig = px.imshow(image_array)
    fig.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

@app.callback(
    Output('text_result', 'children'),
    Input('authors', 'value'),
    Input('title', 'value'),
    Input('categories', 'value')
)
def text_result(authors, title, categories):
    fill_df = merged_df.query("authors.isin(@authors) & Title.isin(@title) & categories.isin(@categories)")
    openai.api_key = openai_Key

    text_to_summarize = " ".join(fill_df['text'].tolist())

    response = openai.ChatCompletion.create(
        model="gpt-4",  # ou "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "Você é um assistente que faz resumos de avaliações de livros."},
            {"role": "user", "content": f"Faça um resumo das seguintes avaliações e retorne os princiapis pontos e conceitos traduzido para português-br: {text_to_summarize}"}
        ]
    )

    # Extrair o texto do resumo gerado
    summary = response['choices'][0]['message']['content']
    return summary

if __name__ == '__main__':
    app.run_server()