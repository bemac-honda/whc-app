# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
import pandas as pd

whc = pd.read_csv('data/whc-sites-2019.csv')
r = whc['region_en'].unique()
regions = np.append('All over the world', r)
categories = whc['category'].unique()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

""" box_style = {'width': '20%',
             'display': 'inline-block',
             'backgroundColor': 'aqua',
             'padding': '1%',
             'margin': '2%',
             'borderRadius': 20,
             'verticalAlign': 'top', } """


app.layout = html.Div([
    html.H3(children='World Heritage Cite (2019)',
            style={'textAlign': 'left'}),

    html.Div([
        html.Div([
            html.Label('Region Select'),
            dcc.Dropdown(id='region',
                         options=[{'label': i, 'value': i} for i in regions],
                         value='All over the world',
                         style={'width': '50%', 'marginLeft': 15}
                         ),
        ]),

        html.Div([
            html.Label('Category Select'),
            dcc.Checklist(id='category',
                          options=[{'label': i, 'value': i}
                                   for i in categories],
                          value=['Cultural', 'Natural', 'Mixed'],
                          style={'marginLeft': 30}
                          ),
        ]),

        html.Div([
            html.Div(id='whc-number',),
        ], ),

    ], style={'columnCount': 1}),

    dcc.Graph(id='whc-map', style={'margin': '1%'})
])


@ app.callback(
    Output('whc-map', 'figure'),
    Output('whc-number', 'children'),
    Input('region', 'value'),
    Input('category', 'value'))
def update_map(region, category):
    if region == 'All over the world':
        whc_r = whc
    else:
        whc_r = whc[whc['region_en'] == region]

    whc_rc = whc_r[whc_r['category'].isin(category)]

    fig = px.scatter_mapbox(whc_rc, lat='latitude', lon='longitude', hover_name='name_en', hover_data=['date_inscribed', 'states_name_en', 'region_en', 'category'],
                            color_discrete_sequence=['fuchsia'], zoom=3, height=300)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig, "Number of World Heritage Cites: {}".format(len(whc_rc))


if __name__ == '__main__':
    app.run_server(debug=True)
